import streamlit as st
from datetime import datetime
from config import SPECIALTIES, EXPERIENCE_LEVELS, OCTA_EXPERIENCE, AI_FAMILIARITY, LABELS
import io
import base64
import textwrap
from PIL import ImageChops, Image
import numpy as np

def render_welcome_page():
    welcome_message = textwrap.dedent("""
        Welcome and thank you for participating in this study. You will be presented with a series of OCT-A scans. For each scan, we will provide a classification and an explanation. Your task is to assess the quality of the classification and explanation.

        The whole process should take approximately 30 minutes to complete.
    """)
    st.markdown(
        f'<div class="welcome-container" style="font-size: 18px; margin: 2rem 0;">{welcome_message}</div>',
        unsafe_allow_html=True
    )
    if st.button("Start Assessment", type="primary", use_container_width=True):
        st.session_state.assessment_started = True
        st.rerun()

def render_post_questionnaire():
    st.markdown("Please provide the information below. This data is collected anonymously and will only be reported in aggregate.")
    
    with st.form(key="demographics_form"):
        user_name = st.text_input("Full Name (for tracking purposes, will not be published)")
        institution = st.text_input("Institution/Hospital")
        col1, col2 = st.columns(2)
        with col1:
            specialty = st.selectbox("Medical Specialty", SPECIALTIES)
            years_experience = st.selectbox("Years of Clinical Experience", EXPERIENCE_LEVELS)
        with col2:
            octa_experience = st.selectbox("Experience with OCTA Imaging", OCTA_EXPERIENCE)
            ai_familiarity = st.selectbox("Familiarity with AI in Medical Imaging", AI_FAMILIARITY)
        
        submitted = st.form_submit_button("Submit and Complete Study", type="primary", use_container_width=True)
        if submitted:
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
                st.session_state.demographics_submitted = True
                st.rerun()
            else:
                st.error("Please enter your name to complete the submission.")

def render_ai_classification():
    if st.session_state.image_loaded and st.session_state.current_label:
        full_name = {
            "PDR": "Proliferative Diabetic Retinopathy",
            "NPDR": "Non-Proliferative Diabetic Retinopathy",
            "Healthy": "Healthy Retina"
        }.get(st.session_state.current_label, "Unknown Classification")
        st.markdown(f"""
        <div class="ai-classification-box">
            <div class="classification-main">{st.session_state.current_label}</div>
            <div class="classification-fullname">{full_name}</div>
        </div>
        """, unsafe_allow_html=True)

def _image_to_html(img):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f'<img src="data:image/png;base64,{img_str}" style="width:100%;border-radius:0px;" alt="Image"/>'

def _crop_whitespace(img, threshold=245, margin=0):
    """Crop near-white padding from image edges.

    Args:
        img: PIL.Image
        threshold: 0-255 grayscale value; pixels < threshold considered foreground.
        margin: extra pixels to retain around detected content.
    """
    try:
        gray = img.convert('L')
        arr = np.array(gray)
        # Foreground mask: anything darker than threshold
        mask = arr < threshold
        if not mask.any():
            return img  # nothing but white
        ys, xs = np.where(mask)
        y0, y1 = ys.min(), ys.max()
        x0, x1 = xs.min(), xs.max()
        # Apply optional margin
        y0 = max(y0 - margin, 0)
        x0 = max(x0 - margin, 0)
        y1 = min(y1 + margin, arr.shape[0]-1)
        x1 = min(x1 + margin, arr.shape[1]-1)
        # Add 1 to include last index in crop box
        cropped = img.crop((x0, y0, x1 + 1, y1 + 1))
        # Avoid accidental over-crop (e.g., if crop removed < 2px border total)
        if abs(cropped.width - img.width) <= 2 and abs(cropped.height - img.height) <= 2:
            return img
        return cropped
    except Exception:
        return img

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
    st.markdown("### Explanation")
    if et in ("graph", "gradcam"):
        # Show explanation image (crop white borders for graph explanations and maintain width)
        exp_img = st.session_state.current_explanation
        if et == "graph" and exp_img is not None:
            exp_img = _crop_whitespace(exp_img)
            try:
                # Match original OCTA image width
                if 'current_image' in st.session_state and st.session_state.current_image is not None:
                    target_w = st.session_state.current_image.width
                    if target_w > 0 and exp_img.width != target_w:
                        new_h = int(exp_img.height * (target_w / exp_img.width))
                        exp_img = exp_img.resize((target_w, max(new_h,1)), Image.LANCZOS)
            except Exception:
                pass
        html = _image_to_html(exp_img)
        st.markdown(html, unsafe_allow_html=True)
        # Horizontal color bar legend
        st.markdown(
            """
            <div style='width:100%;margin-top:6px;'>
              <div style='height:18px;width:100%;background:linear-gradient(to right, rgba(0,0,255,0.85), #00ffff, #00ff00, yellow, #ff7f00, #ff0000);border:1px solid #999;border-radius:4px;'></div>
              <div style='display:flex;justify-content:space-between;font-size:11px;color:#555;margin-top:2px;'>
                <span>Less Important</span>
                <span>More Important</span>
              </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        csv_content = st.session_state.current_csv_content
        if csv_content:
            try:
                lines = csv_content.strip().split('\n')
                feature_names = {
                    "volume": "Vessel Volume", "length": "Vessel Length", "node1_degree": "Inward Connections",
                    "node2_degree": "Outward Connections", "avgCrossSection": "Average Cross-Section",
                    "distance": "Node Distance", "curveness": "Vessel Curvature", "avgRadiusAvg": "Average Radius",
                    "avgRadiusStd": "Radius Variation", "roundnessAvg": "Vessel Roundness",
                    "minRadiusAvg": "Minimum Radius", "hetero_degree": "Heterogeneous Degree",
                }
                feats = []
                try:
                    start = lines.index("Important Features for the Entire Graph:") + 1
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
                            display_name = feature_names.get(feature_name, feature_name.replace("_", " ").title())
                            feats.append({"Feature": display_name, "Importance": f"{float(importance):.3f}"})
                if feats:
                    top_names = [f["Feature"] for f in feats[:3]]
                    if len(top_names) == 1:
                        sentence = f"The key feature leading to this prediction is {top_names[0]}."
                    elif len(top_names) == 2:
                        sentence = f"The two features that most influenced this prediction are {top_names[0]} and {top_names[1]}."
                    else:
                        sentence = (f"The top three features contributing to this prediction are "
                                    f"{top_names[0]}, {top_names[1]}, and {top_names[2]}.")
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
        q2 = st.radio("**2. Rate your confidence in this prediction.**", likert, key=f"q2_{st.session_state.assessments_count}", horizontal=True)
        st.session_state.responses['confidence'] = q2
        q3 = st.radio("**3. Is the explanation highlighting important anatomical or pathological features?**", likert, key=f"q3_{st.session_state.assessments_count}", horizontal=True)
        st.session_state.responses['features_highlighted'] = q3
        q4 = st.radio("**4. Is this explanation highlighting areas that are relevant to the diagnosis?**", likert, key=f"q4_{st.session_state.assessments_count}", horizontal=True)
        st.session_state.responses['localization_correct'] = q4
        q5 = st.radio("**5. Do you like this kind of explanation?**", likert, key=f"q5_{st.session_state.assessments_count}", horizontal=True)
        st.session_state.responses['explanation_like'] = q5
        q6 = st.radio("**6. Does the explanation increase your confidence in the model's prediction?**", likert, key=f"q6_{st.session_state.assessments_count}", horizontal=True)
        st.session_state.responses['trust_increased'] = q6
        q7 = st.radio("**7. Does this prediction + explanation help you interpret this image?**", likert, key=f"q7_{st.session_state.assessments_count}", horizontal=True)
        st.session_state.responses['interpret_help'] = q7

def render_footer():
    st.markdown("---")
    st.markdown(f"""
    <p style="text-align: center; color: #666; font-size: 12px; margin-top: 5px;">
        OCTA DR Classification v2.0 | For Research Purposes Only
    </p>
    """, unsafe_allow_html=True)