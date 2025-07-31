import streamlit as st
from datetime import datetime
import uuid

def initialize_session_state():
    if "assessment_started" not in st.session_state:
        st.session_state.assessment_started = False
    if "demographics_submitted" not in st.session_state:
        st.session_state.demographics_submitted = False
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if "user_info" not in st.session_state:
        st.session_state.user_info = {}
    if "image_loaded" not in st.session_state:
        st.session_state.image_loaded = False
    if "responses" not in st.session_state:
        st.session_state.responses = {}
    if "current_image" not in st.session_state:
        st.session_state.current_image = None
    if "current_image_path" not in st.session_state:
        st.session_state.current_image_path = None
    if "current_label" not in st.session_state:
        st.session_state.current_label = None
    if "current_explanation" not in st.session_state:
        st.session_state.current_explanation = None
    if "current_explanation_type" not in st.session_state:
        st.session_state.current_explanation_type = None
    if "current_csv_content" not in st.session_state:
        st.session_state.current_csv_content = None
    if "assessments_count" not in st.session_state:
        st.session_state.assessments_count = 0
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "all_cases_completed" not in st.session_state:
        st.session_state.all_cases_completed = False
    if "case_start_time" not in st.session_state:
        st.session_state.case_start_time = None
    if "data_loaded" not in st.session_state:
        st.session_state.data_loaded = False
    if "entries" not in st.session_state:
        st.session_state.entries = []
    if "file_cache" not in st.session_state:
        st.session_state.file_cache = {}
    if "next_case_data" not in st.session_state:
        st.session_state.next_case_data = None

def update_current_image(
    image, label, explanation, explanation_type, image_path, csv_content
):
    st.session_state.current_image = image
    st.session_state.current_label = label
    st.session_state.current_explanation = explanation
    st.session_state.current_explanation_type = explanation_type
    st.session_state.current_image_path = image_path
    st.session_state.current_csv_content = csv_content
    st.session_state.image_loaded = True
    st.session_state.chat_history = []
    st.session_state.case_start_time = datetime.now()
    if explanation_type == "text" and explanation:
        st.session_state.chat_history.append(
            {
                "role": "ai",
                "content": explanation,
                "timestamp": datetime.now().strftime("%H:%M"),
            }
        )

def set_current_case_from_dict(case_data):
    if case_data:
        update_current_image(
            case_data['image'],
            case_data['label'],
            case_data['explanation'],
            case_data['explanation_type'],
            case_data['image_path'],
            case_data['csv_content']
        )
    else:
        st.session_state.image_loaded = False

def clear_responses():
    st.session_state.responses = {}

def increment_assessment_count():
    st.session_state.assessments_count += 1

def add_chat_message(role, content):
    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.chat_history.append(
        {"role": role, "content": content, "timestamp": timestamp}
    )