import json
import os
from PIL import Image
import streamlit as st
from config import OCTA_DIR, ENTRIES_FILE

def load_octa_entry():
    if 'entries' not in st.session_state:
        with open(ENTRIES_FILE, 'r') as f:
            st.session_state.entries = json.load(f)
    if 'entry_index' not in st.session_state:
        st.session_state.entry_index = 0
    if not st.session_state.entries:
        st.error(f"No entries in {ENTRIES_FILE}")
        return None, None, None, None, None, None
    
    # Check if the index is out of bounds
    if st.session_state.entry_index >= len(st.session_state.entries):
        return None, None, None, None, None, None 

    entry = st.session_state.entries[st.session_state.entry_index]
    st.session_state.entry_index += 1
    
    image_path = entry['image_id']
    try:
        image = Image.open(image_path)
    except Exception as e:
        st.error(f"Error loading image: {e}")
        return None, None, None, None, None, None
    
    label = entry['label']
    explanation_type = entry.get('explanation_type', 'text')
    exp = entry['explanation']
    
    if explanation_type in ['image', 'graph', 'gradcam']:
        exp_path = exp
        try:
            explanation = Image.open(exp_path)
        except Exception as e:
            st.error(f"Error loading explanation image: {e}")
            explanation = None
    else:
        explanation = exp
    
    csv_path = entry.get('csv_path')
    
    return image, label, explanation, explanation_type, image_path, csv_path