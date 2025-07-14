import glob
import os
import random
from PIL import Image
import streamlit as st
from config import OCTA_DIR, LABELS, EXPLANATIONS

def load_random_octa_image():
    try:
        image_files = glob.glob(os.path.join(OCTA_DIR, "*.png"))
        
        available_images = [img for img in image_files if img not in st.session_state.seen_images]
        
        if not available_images:
            st.session_state.seen_images = []
            available_images = image_files
        
        if not available_images:
            st.error(f"No PNG files found in {OCTA_DIR}")
            return None, None, None, None
        
        selected_image_path = random.choice(available_images)
        st.session_state.seen_images.append(selected_image_path)
        
        selected_label = random.choice(LABELS)
        selected_explanation = EXPLANATIONS[selected_label]
        
        image = Image.open(selected_image_path)
        
        return image, selected_label, selected_explanation, selected_image_path
    
    except Exception as e:
        st.error(f"Error loading image: {str(e)}")
        return None, None, None, None