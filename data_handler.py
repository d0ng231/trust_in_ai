import json
import os
from datetime import datetime
import streamlit as st
from config import OUTPUT_DIR

def save_assessment_to_json(assessment_data):
    user_name = st.session_state.user_info.get('name', 'unknown').replace(' ', '_')
    filename = f"{user_name}_assessments.json"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            all_data = json.load(f)
        
        all_data['assessments'].append(assessment_data)
        all_data['total_assessments'] = len(all_data['assessments'])
        all_data['last_updated'] = datetime.now().isoformat()
    else:
        all_data = {
            'user_info': st.session_state.user_info,
            'session_started': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat(),
            'total_assessments': 1,
            'assessments': [assessment_data]
        }
    
    with open(filepath, 'w') as f:
        json.dump(all_data, f, indent=4)
    
    return filepath

def prepare_assessment_data():
    return {
        "assessment_number": st.session_state.assessments_count + 1,
        "timestamp": datetime.now().isoformat(),
        "image_filename": os.path.basename(st.session_state.current_image_path),
        "ai_classification": st.session_state.current_label,
        "responses": st.session_state.responses
    }