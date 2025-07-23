import streamlit as st
from datetime import datetime
from styles import CUSTOM_CSS
from state_manager import (
    initialize_session_state,
    update_current_image,
    clear_responses,
    increment_assessment_count,
    add_chat_message,
)
from data_handler import save_assessment_to_json, prepare_assessment_data
from image_loader import load_octa_entry
from components import (
    render_pre_questionnaire,
    render_ai_classification,
    render_image_column,
    render_explanation_column,
    render_questions_column,
    render_footer,
)
from inference import generate_explanation, ask_question
from config import GENERATE_LIVE_EXPLANATION
import textwrap


def render_chat_interface():
    st.markdown("### AI Explanation")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


    parts = [
        '<div class="chat-box" '
        'style="height:400px;overflow-y:auto;'
        'border:1px solid #e6e6e6;border-radius:5px;'
        'padding:10px;margin-top:5px;">'
    ]

    if st.session_state.chat_history:
        for msg in st.session_state.chat_history:
            role_class = "user-message" if msg["role"] == "user" else "ai-message"
            who        = "You" if msg["role"] == "user" else "AI"
            parts.append(textwrap.dedent(f"""
                <div class="chat-message {role_class}">
                    <div class="message-content">
                        <strong>{who}:</strong><br>{msg["content"]}
                    </div>
                </div>
            """))
    else:
        parts.append(textwrap.dedent("""
            <div class="chat-placeholder">
              <p>💡 Ask me anything about this OCTA scan!</p>
              <p>Examples:</p>
              <ul>
                <li>What signs of diabetic retinopathy do you see?</li>
                <li>Explain the vessel patterns in this image</li>
                <li>What areas show abnormal vasculature?</li>
              </ul>
            </div>
        """))

    parts.append("</div>")  
    st.markdown("".join(parts), unsafe_allow_html=True)

    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])
        with col1:
            q = st.text_input("Type your question.", label_visibility="collapsed")
        with col2:
            if st.form_submit_button("⬆️", use_container_width=True) and q.strip():
                return q.strip()
    return None

st.set_page_config(
    page_title="Assessment Tool – OCTA DR Classification",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
initialize_session_state()

use_live = GENERATE_LIVE_EXPLANATION

if not st.session_state.user_registered:
    render_pre_questionnaire()
else:
    st.markdown(
        f"**Name:** {st.session_state.user_info['name']}  |  **Assessments Completed:** {st.session_state.assessments_count}"
    )
    if not st.session_state.image_loaded:
        img, lbl, expl, etype, path, csv = load_octa_entry()
        if img:
            if use_live:
                expl = generate_explanation(img, lbl)
                etype = "text"
                csv = None
            update_current_image(img, lbl, expl, etype, path, csv)
    col1, col2, col3 = st.columns([1, 1, 1.5], gap="medium")
    with col1:
        render_image_column()
        render_ai_classification()
    with col2:
        if st.session_state.current_explanation_type == "text":
            user_question = render_chat_interface()
            if user_question:
                add_chat_message("user", user_question)
                with st.spinner("thinking…"):
                    try:
                        ai_response = ask_question(
                            st.session_state.current_image,
                            user_question,
                            st.session_state.current_label,
                        )
                        add_chat_message("ai", ai_response)
                        st.rerun()
                    except Exception as e:
                        add_chat_message("ai", f"Error: {e}")
                        st.rerun()
        else:
            render_explanation_column()
    with col3:
        render_questions_column()
    _, col_button, _ = st.columns([1, 1, 1])
    with col_button:
        if st.button("Submit Assessment & Load Next", type="primary", use_container_width=True):
            data = prepare_assessment_data()
            save_assessment_to_json(data)
            increment_assessment_count()
            clear_responses()
            img2, lbl2, expl2, etype2, path2, csv2 = load_octa_entry()
            if img2:
                if use_live:
                    expl2 = generate_explanation(img2, lbl2)
                    etype2 = "text"
                    csv2 = None
                update_current_image(img2, lbl2, expl2, etype2, path2, csv2)
                st.rerun()
            else:
                st.error("No more images available.")
    render_footer()
