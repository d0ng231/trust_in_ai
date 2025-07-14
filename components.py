import streamlit as st
from datetime import datetime
from config import SPECIALTIES, EXPERIENCE_LEVELS, OCTA_EXPERIENCE, AI_FAMILIARITY, LABEL_COLORS

def render_pre_questionnaire():
    with st.container():
        st.markdown('<div class="pre-questionnaire-box">', unsafe_allow_html=True)
        
        user_name = st.text_input("**Full Name**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            specialty = st.selectbox("**Medical Specialty**", SPECIALTIES)
            years_experience = st.selectbox("**Years of Clinical Experience**", EXPERIENCE_LEVELS)
        
        with col2:
            octa_experience = st.selectbox("**Experience with OCTA Imaging**", OCTA_EXPERIENCE)
            ai_familiarity = st.selectbox("**Familiarity with AI in Medical Imaging**", AI_FAMILIARITY)
        
        institution = st.text_input("**Institution/Hospital**", placeholder="Optional")
        
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
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_ai_classification():
    if st.session_state.image_loaded and st.session_state.current_label:
        label = st.session_state.current_label
        color = LABEL_COLORS[label]
        full_name = {
            "PDR": "Proliferative Diabetic Retinopathy",
            "NPDR": "Non-Proliferative Diabetic Retinopathy",
            "Healthy": "Healthy Retina"
        }[label]
        
        st.markdown(f"""
        <div class="ai-classification-box">
            🤖 AI Classification: <span style="color: {color};">{label} - {full_name}</span>
        </div>
        """, unsafe_allow_html=True)

def render_image_column():
    st.markdown("### 📊 OCTA Scan")
    if st.session_state.image_loaded and st.session_state.current_image:
        st.image(st.session_state.current_image, use_container_width=True, caption="OCTA DCP Image")

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
    
    with st.container():
        st.markdown('<div class="questions-box">', unsafe_allow_html=True)
        
        q1 = st.radio(
            "**1. Is the model prediction correct?**",
            ["Yes", "No", "Uncertain"],
            key=f"q1_{st.session_state.assessments_count}",
            horizontal=True
        )
        st.session_state.responses['prediction_correct'] = q1
        
        q2 = st.radio(
            "**2. Does the explanation increase your trust in the model?**",
            ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"],
            key=f"q2_{st.session_state.assessments_count}"
        )
        st.session_state.responses['trust_increased'] = q2
        
        q3 = st.radio(
            "**3. Is the explanation localizing important regions in the image?**",
            ["Yes", "No", "Partially"],
            key=f"q3_{st.session_state.assessments_count}",
            horizontal=True
        )
        st.session_state.responses['localization_correct'] = q3
        
        q4 = st.radio(
            "**4. Is the explanation highlighting important features?**",
            ["Yes", "No", "Partially"],
            key=f"q4_{st.session_state.assessments_count}",
            horizontal=True
        )
        st.session_state.responses['features_highlighted'] = q4
        
        q5 = st.radio(
            "**5. Will this AI save your time?**",
            ["Yes", "No", "Uncertain"],
            key=f"q5_{st.session_state.assessments_count}",
            horizontal=True
        )
        st.session_state.responses['time_saving'] = q5
        
        st.markdown('<p class="confidence-label">6. Rate your confidence in this AI assessment:</p>', unsafe_allow_html=True)
        confidence = st.slider(
            "Confidence",
            min_value=0,
            max_value=100,
            value=50,
            step=5,
            format="%d%%",
            label_visibility="collapsed",
            key=f"confidence_{st.session_state.assessments_count}"
        )
        st.session_state.responses['confidence'] = confidence
        
        if confidence < 30:
            conf_color = "#d32f2f"
        elif confidence < 70:
            conf_color = "#ff9800"
        else:
            conf_color = "#4caf50"
            
        st.markdown(f'<p style="text-align: center; font-size: 20px; color: {conf_color}; font-weight: bold; margin-top: 0.25rem;">{confidence}% Confidence</p>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_footer():
    st.markdown("---")
    user_file = f"{st.session_state.user_info.get('name', 'User').replace(' ', '_')}_assessments.json" if st.session_state.user_registered else ""
    st.markdown(f"""
    <p style='text-align: center; color: #666; font-size: 12px; margin-top: 5px;'>
        OCTA DR Classification v1.0 | For Research Purposes Only<br>
    </p>
    """, unsafe_allow_html=True)