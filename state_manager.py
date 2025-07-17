import streamlit as st

def initialize_session_state():
    if 'user_registered' not in st.session_state:
        st.session_state.user_registered = False
    if 'user_info' not in st.session_state:
        st.session_state.user_info = {}
    if 'image_loaded' not in st.session_state:
        st.session_state.image_loaded = False
    if 'responses' not in st.session_state:
        st.session_state.responses = {}
    if 'current_image' not in st.session_state:
        st.session_state.current_image = None
    if 'current_image_path' not in st.session_state:
        st.session_state.current_image_path = None
    if 'current_label' not in st.session_state:
        st.session_state.current_label = None
    if 'current_explanation' not in st.session_state:
        st.session_state.current_explanation = None
    if 'current_explanation_type' not in st.session_state:
        st.session_state.current_explanation_type = None
    if 'current_csv_path' not in st.session_state:
        st.session_state.current_csv_path = None
    if 'assessments_count' not in st.session_state:
        st.session_state.assessments_count = 0
    if 'seen_images' not in st.session_state:
        st.session_state.seen_images = []

def update_current_image(image, label, explanation, explanation_type, image_path, csv_path):
    st.session_state.current_image = image
    st.session_state.current_label = label
    st.session_state.current_explanation = explanation
    st.session_state.current_explanation_type = explanation_type
    st.session_state.current_image_path = image_path
    st.session_state.current_csv_path = csv_path
    st.session_state.image_loaded = True

def clear_responses():
    st.session_state.responses = {}

def increment_assessment_count():
    st.session_state.assessments_count += 1
