import streamlit as st
import os
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
    page_title="Trust-in-AI Assessment Tool - OCTA DR Classification",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

initialize_session_state()

st.markdown("<h1>👁️ Trust-in-AI Assessment Tool</h1>", unsafe_allow_html=True)

if not st.session_state.user_registered:
    render_pre_questionnaire()
else:
    st.markdown(f"**Clinician:** {st.session_state.user_info['name']} | **Assessments Completed:** {st.session_state.assessments_count}")
    
    if not st.session_state.image_loaded:
        image, label, explanation, image_path = load_random_octa_image()
        if image:
            update_current_image(image, label, explanation, image_path)
    
    render_ai_classification()
    
    col1, col2, col3 = st.columns([1, 1, 1], gap="medium")
    
    with col1:
        render_image_column()
    
    with col2:
        render_explanation_column()
    
    with col3:
        render_questions_column()
    
    st.markdown("<br>", unsafe_allow_html=True)
    col_empty1, col_button, col_empty2 = st.columns([1, 1, 1])
    with col_button:
        if st.button("Submit Assessment & Load Next", type="primary", use_container_width=True):
            required_keys = ['prediction_correct', 'trust_increased', 'localization_correct', 
                           'features_highlighted', 'time_saving', 'confidence']
            
            if all(key in st.session_state.responses for key in required_keys):
                assessment_data = prepare_assessment_data()
                saved_file = save_assessment_to_json(assessment_data)
                
                increment_assessment_count()
                clear_responses()
                
                image, label, explanation, image_path = load_random_octa_image()
                if image:
                    update_current_image(image, label, explanation, image_path)
                    st.rerun()
                else:
                    st.error("No more images available.")
            else:
                st.error("⚠️ Please answer all questions before submitting.")

render_footer()