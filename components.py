import streamlit as st
from datetime import datetime
from config import SPECIALTIES, EXPERIENCE_LEVELS, OCTA_EXPERIENCE, AI_FAMILIARITY, LABELS
import textwrap
import io
import base64

def render_pre_questionnaire():
    welcome_message = textwrap.dedent("""
        Welcome and thank you for participating in this study. Please answer each question as accurately as you can. Your responses will be processed anonymously and reported only in aggregate. The whole process should take approximately 30 minutes to complete. If you need to pause, you may return and continue later.
    """)

    st.markdown(
        f'<div class="welcome-container">{welcome_message}</div>',
        unsafe_allow_html=True
    )

    user_name = st.text_input("Full Name")
    col1, col2 = st.columns(2)
    with col1:
        specialty = st.selectbox("Medical Specialty", SPECIALTIES)
        years_experience = st.selectbox("Years of Clinical Experience", EXPERIENCE_LEVELS)
    with col2:
        octa_experience = st.selectbox("Experience with OCTA Imaging", OCTA_EXPERIENCE)
        ai_familiarity = st.selectbox("Familiarity with AI in Medical Imaging", AI_FAMILIARITY)
    institution = st.text_input("Institution/Hospital")

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
        full_name = {
            "PDR": "Proliferative Diabetic Retinopathy",
            "NPDR": "Non-Proliferative Diabetic Retinopathy",
            "Healthy": "Healthy Retina"
        }[st.session_state.current_label]
        
        st.markdown(f"""
        <div class="ai-classification-box">
            <div class="classification-title">AI Classification</div>
            <div class="classification-main">{st.session_state.current_label}</div>
            <div class="classification-fullname">{full_name}</div>
        </div>
        """, unsafe_allow_html=True)

def _image_to_html(img):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f'<img src="data:image/png;base64,{img_str}" style="width:100%;border-radius:0px;" alt="Image"/>'

def render_image_column():
    st.markdown("### OCTA Scan")
    if st.session_state.image_loaded and st.session_state.current_image:
        html = _image_to_html(st.session_state.current_image)
        st.markdown(html, unsafe_allow_html=True)

def render_explanation_column():
    if not st.session_state.image_loaded:
        return
    et = st.session_state.current_explanation_type
    if et == "text":
        return
    st.markdown("### AI Explanation")
    if et == "graph":
        html = _image_to_html(st.session_state.current_explanation)
        st.markdown(html, unsafe_allow_html=True)
        cp = st.session_state.current_csv_path
        if cp:
            try:
                with open(cp, "r") as f:
                    lines = [l.rstrip("\n") for l in f]
                feature_names = {
                    "volume": "Vessel Volume",
                    "length": "Vessel Length",
                    "node1_degree": "Inward Connections",
                    "node2_degree": "Outward Connections",
                    "avgCrossSection": "Average Cross-Section",
                    "distance": "Node Distance",
                    "curveness": "Vessel Curvature",
                    "avgRadiusAvg": "Average Radius",
                    "avgRadiusStd": "Radius Variation",
                    "roundnessAvg": "Vessel Roundness",
                    "minRadiusAvg": "Minimum Radius",
                    "hetero_degree": "Heterogeneous Degree",
                }
                feats = []
                try:
                    start = lines.index(
                        "Important Features for the Entire Graph:"
                    ) + 1
                except ValueError:
                    start = -1
                if start >= 0:
                    header_found = False
                    for line in lines[start:]:
                        if not line.strip() or line.startswith("Top k"):
                            break
                        if line.startswith("feature,importance"):
                            header_found = True
                            continue
                        if not header_found:
                            continue
                        parts = [p.strip() for p in line.split(",", 2)]
                        if len(parts) >= 2:
                            feature_name = parts[0]
                            importance = parts[1]
                            display_name = feature_names.get(
                                feature_name,
                                feature_name.replace("_", " ").title(),
                            )
                            feats.append(
                                {
                                    "Feature": display_name,
                                    "Importance": f"{float(importance):.3f}",
                                }
                            )
                    if feats:
                        top_names = [f["Feature"] for f in feats[:3]]
                        if len(top_names) == 1:
                            sentence = f"The key feature leading to this prediction is {top_names[0]}."
                        elif len(top_names) == 2:
                            sentence = f"The two features that most influenced this prediction are {top_names[0]} and {top_names[1]}."
                        else:
                            sentence = (
                                f"The top three features contributing to this prediction are "
                                    f"{top_names[0]}, {top_names[1]}, and {top_names[2]}."
                                )
                            st.markdown(sentence)
            except Exception as e:
                st.warning(f"Could not load feature data: {e}")
    else:
        html = _image_to_html(st.session_state.current_explanation)
        st.markdown(html, unsafe_allow_html=True)

def render_questions_column():
    st.markdown("### Assessment Questions")
    st.markdown("**For questions 2–7, please rate your agreement on a scale from 1 (Strongly Disagree) to 5 (Strongly Agree).**")
    likert = ["1", "2", "3", "4", "5"]
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
        q6 = st.radio("**6. Does the explanation increase your trust in the model's prediction?**", likert, key=f"q6_{st.session_state.assessments_count}", horizontal=True)
        st.session_state.responses['trust_increased'] = q6
        q7 = st.radio("**7. Will this AI help you save time?**", likert, key=f"q7_{st.session_state.assessments_count}", horizontal=True)
        st.session_state.responses['time_saving'] = q7

def render_footer():
    st.markdown("---")
    st.markdown(f"""
    <p style="text-align: center; color: #666; font-size: 12px; margin-top: 5px;">
        OCTA DR Classification v1.5 | For Research Purposes Only
    </p>
    """, unsafe_allow_html=True)