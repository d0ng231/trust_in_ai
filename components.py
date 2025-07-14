import streamlit as st
from datetime import datetime
from config import SPECIALTIES, EXPERIENCE_LEVELS, OCTA_EXPERIENCE, AI_FAMILIARITY, LABELS

def render_pre_questionnaire():
    with st.container():
        st.markdown("""
        **Welcome!**

        This short questionnaire collects your clinical background before guiding you through evaluating AI-generated classifications of OCTA scans.  
        Please provide your information below to begin.
        """)
        user_name = st.text_input("Full Name")
        col1, col2 = st.columns(2)
        with col1:
            specialty = st.selectbox("Medical Specialty", SPECIALTIES)
            years_experience = st.selectbox("Years of Clinical Experience", EXPERIENCE_LEVELS)
        with col2:
            octa_experience = st.selectbox("Experience with OCTA Imaging", OCTA_EXPERIENCE)
            ai_familiarity = st.selectbox("Familiarity with AI in Medical Imaging", AI_FAMILIARITY)
        institution = st.text_input("Institution/Hospital", placeholder="Optional")
        if st.button("Start Assessment", type="primary", use_container_width=True):
            if user_name:
                st.session_state.user_info = {
                    "name": user_name,
                    "specialty": specialty,
                    "years_experience": years_experience,
                    "octa_experience": octa_experience,
                    "ai_familiarity": ai_familiarity,
                    "institution": institution,
                    "registration_timestamp": datetime.now().isoformat()
                }
                st.session_state.user_registered = True
                st.rerun()
            else:
                st.error("Please enter your name to continue.")

def render_ai_classification():
    if st.session_state.image_loaded and st.session_state.current_label:
        label = st.session_state.current_label
        full_name = {
            "PDR": "Proliferative Diabetic Retinopathy",
            "NPDR": "Non-Proliferative Diabetic Retinopathy",
            "Healthy": "Healthy Retina"
        }[label]
        st.markdown(f"""
        <div class="ai-classification-box">
            AI Classification: <span style="color: #000000;">{label} — {full_name}</span>
        </div>
        """, unsafe_allow_html=True)

def render_image_column():
    st.markdown("### 📊 OCTA Scan")
    if st.session_state.image_loaded and st.session_state.current_image:
        st.image(st.session_state.current_image, use_container_width=True, caption="DCP Image")

def render_explanation_column():
    st.markdown("### 📝 AI Explanation")
    if st.session_state.image_loaded and st.session_state.current_explanation:
        st.text_area(
            "Model Explanation",
            value=st.session_state.current_explanation,
            height=400,
            label_visibility="collapsed",
            disabled=True
        )

def render_questions_column():
    st.markdown("### ✅ Assessment Questions")
    st.markdown("**For questions 2–7, please rate your agreement on a scale from –2 (Strongly Disagree) to +2 (Strongly Agree).**")
    likert = ["-2", "-1", "0", "1", "2"]
    with st.container():
        q1 = st.radio("**1. Is the model's prediction correct?**", ["Yes", "No"], key=f"q1_{st.session_state.assessments_count}", horizontal=True)
        st.session_state.responses['prediction_correct'] = q1
        if q1 == "No":
            current = st.session_state.current_label
            others = [l for l in LABELS if l != current]
            q1b = st.radio("**Please specify the correct label:**", others, key=f"correct_label_{st.session_state.assessments_count}", horizontal=True)
            st.session_state.responses['correct_label'] = q1b


        q2 = st.radio("**2. Rate your confidence in this AI assessment.**", likert, key=f"q2_{st.session_state.assessments_count}", horizontal=True)
        st.session_state.responses['confidence'] = q2

        q3 = st.radio("**3. Is the explanation highlighting important features?**", likert, key=f"q3_{st.session_state.assessments_count}", horizontal=True)
        st.session_state.responses['features_highlighted'] = q3

        q4 = st.radio("**4. Is this explanation highlighting areas that are relevant to the diagnosis?**", likert, key=f"q4_{st.session_state.assessments_count}", horizontal=True)
        st.session_state.responses['localization_correct'] = q4

        q5 = st.radio("**5. Do you like this kind of explanation?**", likert, key=f"q5_{st.session_state.assessments_count}", horizontal=True)
        st.session_state.responses['explanation_like'] = q5

        q6 = st.radio("**6. Does the explanation increase your trust in the model's diagnosis?**", likert, key=f"q6_{st.session_state.assessments_count}", horizontal=True)
        st.session_state.responses['trust_increased'] = q6

        q7 = st.radio("**7. Will this AI help you save time?**", likert, key=f"q7_{st.session_state.assessments_count}", horizontal=True)
        st.session_state.responses['time_saving'] = q7

def render_footer():
    st.markdown("---")
    st.markdown(f"""
    <p style="text-align: center; color: #666; font-size: 12px; margin-top: 5px;">
        OCTA DR Classification v1.0 | For Research Purposes Only
    </p>
    """, unsafe_allow_html=True)
