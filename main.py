import streamlit as st
from datetime import datetime
from styles import CUSTOM_CSS
from state_manager import initialize_session_state, update_current_image, clear_responses, increment_assessment_count
from data_handler import save_assessment_to_json, prepare_assessment_data
from image_loader import load_octa_entry
from components import (
    render_pre_questionnaire,
    render_ai_classification,
    render_image_column,
    render_explanation_column,
    render_questions_column,
    render_footer
)
from inference import classify_and_explain, ask_question

def add_chat_message(role, content):
    timestamp = datetime.now().strftime("%H:%M")
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    st.session_state.chat_history.append({
        "role": role,
        "content": content,
        "timestamp": timestamp
    })

def render_chat_interface():
    st.markdown("### 💬 Chat with this model")
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    chat_container = st.container()
    with chat_container:
        if st.session_state.chat_history:
            for i, message in enumerate(st.session_state.chat_history):
                if message['role'] == 'user':
                    st.markdown(f"""
                    <div class="chat-message user-message">
                        <div class="message-content">
                            <strong>You:</strong><br>
                            {message['content']}
                        </div>
                        <div class="message-time">{message['timestamp']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-message ai-message">
                        <div class="message-content">
                            <strong>AI:</strong><br>
                            {message['content']}
                        </div>
                        <div class="message-time">{message['timestamp']}</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="chat-placeholder">
                <p>💡 Ask me anything about this OCTA scan!</p>
                <p>Examples:</p>
                <ul>
                    <li>What signs of diabetic retinopathy do you see?</li>
                    <li>Explain the vessel patterns in this image</li>
                    <li>What areas show abnormal vasculature?</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])
        with col1:
            user_input = st.text_input(
                "Type your question...",
                label_visibility="collapsed"
            )
        with col2:
            submit_button = st.form_submit_button("⬆️", use_container_width=True)
        
        if submit_button and user_input.strip():
            return user_input.strip()
    
    return None

def clear_chat_history():
    if st.button("🗑️ Clear Chat", help="Clear conversation history"):
        st.session_state.chat_history = []
        st.rerun()

st.set_page_config(
    page_title="Assessment Tool – OCTA DR Classification",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
initialize_session_state()

use_live = st.sidebar.checkbox("Generate Live Explanation", value=False)

if not st.session_state.user_registered:
    render_pre_questionnaire()
else:
    st.markdown(f"**Name:** {st.session_state.user_info['name']}  |  **Assessments Completed:** {st.session_state.assessments_count}")
    
    if not st.session_state.image_loaded:
        img, lbl, expl, etype, path, csv = load_octa_entry()
        if img:
            if use_live:
                lbl, expl = classify_and_explain(img)
                etype = "text"
                csv = None
            update_current_image(img, lbl, expl, etype, path, csv)
    
    col1, col2, col3 = st.columns([1,1,1.5], gap="medium")
    
    with col1:
        render_image_column()
        render_ai_classification()
    
    with col2:
        render_explanation_column()
        
        st.markdown("---")
        
        user_question = render_chat_interface()
        
        if user_question:
            add_chat_message("user", user_question)
            
            with st.spinner("thinking..."):
                try:
                    ai_response = ask_question(st.session_state.current_image, user_question)
                    add_chat_message("ai", ai_response)
                    st.rerun()
                except Exception as e:
                    add_chat_message("ai", f"Sorry, I encountered an error: {str(e)}")
                    st.rerun()
        
        clear_chat_history()
    
    with col3:
        render_questions_column()
    
    _, col_button, _ = st.columns([1,1,1])
    with col_button:
        if st.button("Submit Assessment & Load Next", type="primary", use_container_width=True):
            data = prepare_assessment_data()
            save_assessment_to_json(data)
            increment_assessment_count()
            clear_responses()
            
            img2, lbl2, expl2, etype2, path2, csv2 = load_octa_entry()
            if img2:
                if use_live:
                    lbl2, expl2 = classify_and_explain(img2)
                    etype2 = "text"
                    csv2 = None
                update_current_image(img2, lbl2, expl2, etype2, path2, csv2)
                st.rerun()
            else:
                st.error("No more images available.")
    
    render_footer()