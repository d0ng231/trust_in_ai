import streamlit as st
from PIL import Image
import io
from data_handler import get_local_path
from config import GENERATE_LIVE_EXPLANATION

def load_octa_entry():
    if 'entry_index' not in st.session_state:
        st.session_state.entry_index = 0
    if not st.session_state.get('entries'):
        st.error("No entries available to load.")
        return None, None, None, None, None, None
    if st.session_state.entry_index >= len(st.session_state.entries):
        return None, None, None, None, None, None
    entry = st.session_state.entries[st.session_state.entry_index]
    st.session_state.entry_index += 1
    drive_image_path = entry['image_id']
    label = entry['label']
    explanation_type = entry.get('explanation_type', 'text')
    exp_path_or_text = entry['explanation']
    drive_csv_path = entry.get('csv_path')
    local_image_path = get_local_path(drive_image_path)
    if not local_image_path or not local_image_path.exists():
        st.error(f"Image file not found locally: {drive_image_path}")
        return None, None, None, None, None, None
    image = Image.open(local_image_path)
    explanation = None
    if explanation_type in ['image', 'graph', 'gradcam']:
        # Always attempt to load image-based explanations regardless of live generation toggle.
        local_exp_path = get_local_path(exp_path_or_text)
        if local_exp_path and local_exp_path.exists():
            explanation = Image.open(local_exp_path)
        else:
            st.warning(f"Explanation image not found: {exp_path_or_text}")
    else:
        # Text explanation: if live generation enabled, defer actual content generation in UI.
        if GENERATE_LIVE_EXPLANATION:
            explanation_type = 'text'
            explanation = None
        else:
            explanation = exp_path_or_text
    csv_content = None
    if drive_csv_path:
        local_csv_path = get_local_path(drive_csv_path)
        if local_csv_path and local_csv_path.exists():
            csv_content = local_csv_path.read_text(encoding='utf-8')
        else:
            st.warning(f"CSV file not found: {drive_csv_path}")
    return image, label, explanation, explanation_type, str(local_image_path), csv_content

def load_and_package_entry():
    img, lbl, expl, et, path, csv_content = load_octa_entry()
    if img:
        return {
            "image": img,
            "label": lbl,
            "explanation": expl,
            "explanation_type": et,
            "image_path": path,
            "csv_content": csv_content
        }
    return None