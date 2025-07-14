import streamlit as st
from styles import CUSTOM_CSS
from state_manager import initialize_session_state, update_current_image, clear_responses, increment_assessment_count
from data_handler import save_assessment_to_json, prepare_assessment_data
from image_loader import load_random_octa_image
from components import (
    render_pre_questionnaire,
    render_ai_classification,
    render_image_column,
    render_explanation_column,
    render_questions_column,
    render_footer
)

st.set_page_config(
    page_title="Assessment Tool – OCTA DR Classification",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

initialize_session_state()

if not st.session_state.user_registered:
    render_pre_questionnaire()
else:
    st.markdown(f"**Name:** {st.session_state.user_info['name']}  |  **Assessments Completed:** {st.session_state.assessments_count}")

    if not st.session_state.image_loaded:
        image, label, explanation, _ = load_random_octa_image()
        if image:
            update_current_image(image, label, explanation, _)

    col1, col2, col3 = st.columns([1,1,1.5], gap="medium")
    with col1:
        render_image_column()
        render_ai_classification()
    with col2:
        render_explanation_column()
    with col3:
        render_questions_column()

    st.markdown("<br>", unsafe_allow_html=True)
    _, col_button, _ = st.columns([1,1,1])
    with col_button:
        if st.button("Submit Assessment & Load Next", type="primary", use_container_width=True):
            data = prepare_assessment_data()
            save_assessment_to_json(data)
            increment_assessment_count()
            clear_responses()
            nxt, lbl, expl, _ = load_random_octa_image()
            if nxt:
                update_current_image(nxt, lbl, expl, _)
                st.rerun()
            else:
                st.error("No more images available.")

    render_footer()
