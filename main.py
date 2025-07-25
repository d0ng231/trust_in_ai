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
from inference import generate_explanation, ask_question_stream
from config import GENERATE_LIVE_EXPLANATION, EVALUATION_MODE
from evaluation import render_evaluation_page

def render_finish_page():
    st.balloons()
    finish_html = f"""
    <div style="text-align: center; padding-top: 3rem;">
        <h1>Thank You!</h1>
        <br>
        <h3>You have completed the assessment.</h3>
        <p style="font-size: 18px;">
            Thank you for your time and valuable input. You assessed a total of <strong>{st.session_state.assessments_count}</strong> cases.
        </p>
        <br>
        <p style="color: #666;">
            You may now close this browser tab.
        </p>
    </div>
    """
    st.markdown(finish_html, unsafe_allow_html=True)


st.set_page_config(
    page_title="Assessment Tool – OCTA DR Classification",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


if EVALUATION_MODE:
    render_evaluation_page()
else:
    initialize_session_state()
    use_live = GENERATE_LIVE_EXPLANATION

    if not st.session_state.user_registered:
        render_pre_questionnaire()
    else:
        if st.session_state.all_cases_completed:
            render_finish_page()
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
                else:
                    st.session_state.all_cases_completed = True
                    st.rerun()

            col1, col2, col3 = st.columns([1, 1, 1.5], gap="medium")
            with col1:
                render_image_column()
                render_ai_classification()
            with col2:
                if st.session_state.current_explanation_type == "text":
                    st.markdown("### AI Explanation")

                    chat_container = st.container(height=470, border=True)

                    for msg in st.session_state.chat_history:
                        with chat_container.chat_message(name=msg["role"]):
                            st.markdown(msg["content"])
                    
                    st.markdown('<p style="font-weight: 500; margin-top: 0.1rem; margin-bottom: 0.1rem;">Suggested Questions:</p>', unsafe_allow_html=True)
                    st.markdown('<div class="suggestion-container">', unsafe_allow_html=True)
                    suggestions = [
                        "What signs of diabetic retinopathy do you see?",
                        "Explain the vessel patterns in this image.",
                        "What areas show abnormal vasculature?",
                    ]
                    prompt_from_button = None
                    for i, suggestion in enumerate(suggestions):
                        if st.button(suggestion, use_container_width=True, key=f"suggestion_{i}"):
                            prompt_from_button = suggestion
                    st.markdown('</div>', unsafe_allow_html=True)

                    prompt = st.chat_input("Type your question...") or prompt_from_button

                    if prompt:
                        add_chat_message("user", prompt)
                        with chat_container.chat_message("user"):
                            st.markdown(prompt)

        
                        with chat_container.chat_message("ai"):
                            response = st.write_stream(
                                ask_question_stream(
                                    st.session_state.current_image,
                                    prompt,
                                    st.session_state.current_label,
                                )
                            )
                        add_chat_message("ai", response)

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
                        st.session_state.all_cases_completed = True
                        st.rerun()
            render_footer()