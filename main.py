import streamlit as st
import random
from styles import CUSTOM_CSS
from state_manager import initialize_session_state, set_current_case_from_dict, clear_responses, increment_assessment_count, add_chat_message
from data_handler import prepare_assessment_data, fetch_metadata, synchronize_drive_data, append_assessment_locally, finalize_and_upload, fetch_password_on_demand
from image_loader import load_and_package_entry
from components import render_welcome_page, render_post_questionnaire, render_ai_classification, render_image_column, render_explanation_column, render_questions_column, render_footer
from inference import ask_question_stream, generate_explanation
from config import GENERATE_LIVE_EXPLANATION
from evaluation import render_evaluation_page

def load_and_manage_cases():
    if not st.session_state.image_loaded:
        if st.session_state.next_case_data:
            set_current_case_from_dict(st.session_state.next_case_data)
            st.session_state.next_case_data = load_and_package_entry()
        else:
            first_case_data = load_and_package_entry()
            if first_case_data:
                set_current_case_from_dict(first_case_data)
                st.session_state.next_case_data = load_and_package_entry()
            else:
                st.session_state.all_cases_completed = True
        
        if not st.session_state.image_loaded:
             st.session_state.all_cases_completed = True
        
        if not st.session_state.all_cases_completed:
            st.rerun()

st.set_page_config(page_title="Assessment Tool", page_icon="🩺", layout="wide", initial_sidebar_state="collapsed")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

initialize_session_state()

with st.sidebar.expander("Evaluation mode", expanded=False):
    pwd = st.text_input("Password", type="password", key="eval_pwd")
    if st.button("Enter", key="eval_enter"):
        drive_password = fetch_password_on_demand()
        if drive_password is None:
            st.error("Evaluation mode is currently unavailable.")
        elif pwd and pwd == drive_password.strip():
            st.session_state.eval_mode = True
            st.success("Evaluation mode activated")
            st.rerun()
        else:
            st.error("Incorrect password")

if st.session_state.get('eval_mode'):
    render_evaluation_page()
elif not st.session_state.assessment_started:
    render_welcome_page()
elif not st.session_state.all_cases_completed:
    if not st.session_state.data_loaded:
        with st.spinner("Preparing assessment... This may take a moment."):
            synchronize_drive_data()
            entries = fetch_metadata()
            if entries:
                random.shuffle(entries)
                st.session_state.entries = entries
                st.session_state.data_loaded = True
            else:
                st.error("Fatal: Could not load assessment metadata.")
                st.stop()
    
    load_and_manage_cases()
    
    if st.session_state.all_cases_completed:
        st.rerun()
    else:
        st.markdown(f"**Case:** {st.session_state.assessments_count + 1} / {len(st.session_state.entries)}  |  **Session ID:** {st.session_state.session_id}")
        c1, c2, c3 = st.columns([1, 1, 1.5], gap="medium")
        with c1:
            render_image_column()
            render_ai_classification()
        with c2:
            if st.session_state.current_explanation_type == "text":
                st.markdown("### Explanation")
                chat = st.container(height=470, border=True)
                # Auto-stream initial explanation if live generation enabled and no AI message yet
                if GENERATE_LIVE_EXPLANATION and not any(m["role"] == "ai" for m in st.session_state.chat_history):
                    init_prompt = (
                        f"Provide a concise explanation for why this OCTA image is classified as {st.session_state.current_label}. "
                        "Reference specific regions or vascular patterns briefly."
                    )
                    with chat.chat_message("ai"):
                        resp = st.write_stream(ask_question_stream(st.session_state.current_image, init_prompt, st.session_state.current_label))
                    add_chat_message("ai", resp)
                else:
                    # Render existing history only when not in the special first-stream case
                    for m in st.session_state.chat_history:
                        with chat.chat_message(name=m["role"]):
                            st.markdown(m["content"])
                st.markdown('<p style="font-weight:500;margin:0.1rem 0;">Suggested Questions:</p>', unsafe_allow_html=True)
                st.markdown('<div class="suggestion-container">', unsafe_allow_html=True)
                sug = ["What signs of diabetic retinopathy do you see?", "Explain the vessel patterns in this image.", "What areas show abnormal vasculature?"]
                pick = None
                for i, s in enumerate(sug):
                    if st.button(s, use_container_width=True, key=f"sug_{i}_{st.session_state.assessments_count}"):
                        pick = s
                st.markdown("</div>", unsafe_allow_html=True)
                prompt = st.chat_input("Type your question...") or pick
                if prompt:
                    add_chat_message("user", prompt)
                    with chat.chat_message("user"):
                        st.markdown(prompt)
                    with chat.chat_message("ai"):
                        resp = st.write_stream(ask_question_stream(st.session_state.current_image, prompt, st.session_state.current_label))
                    add_chat_message("ai", resp)
            else:
                render_explanation_column()
        with c3:
            render_questions_column()
        _, btn_col, _ = st.columns([1, 1, 1])
        with btn_col:
            if st.button("Submit Assessment & Load Next", type="primary", use_container_width=True):
                append_assessment_locally(prepare_assessment_data())
                increment_assessment_count()
                clear_responses()
                st.session_state.image_loaded = False
                st.rerun()
        render_footer()
elif not st.session_state.demographics_submitted:
    render_post_questionnaire()
else:
    with st.spinner("Finalizing and submitting your assessment... Please wait."):
        finalize_and_upload(st.session_state.user_info)
    st.balloons()
    st.markdown(f"<div style='text-align:center;padding-top:3rem'><h1>Thank You!</h1><br><h3>You have successfully completed the assessment.</h3><p style='font-size:18px'>You assessed <strong>{st.session_state.assessments_count}</strong> cases.</p><br><p style='color:#666'>You may now close this tab.</p></div>", unsafe_allow_html=True)