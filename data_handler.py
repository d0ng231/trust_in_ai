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
        try:
            with open(filepath, 'r') as f:
                content = f.read().strip()
                if content:  # Check if file has content
                    all_data = json.loads(content)
                else:
                    # File exists but is empty, create new structure
                    all_data = None
        except (json.JSONDecodeError, Exception) as e:
            st.warning(f"Existing file corrupted, creating new file: {e}")
            all_data = None
        
        if all_data:
            all_data['assessments'].append(assessment_data)
            all_data['total_assessments'] = len(all_data['assessments'])
            all_data['last_updated'] = datetime.now().isoformat()
        else:
            # Create new structure if file was empty or corrupted
            all_data = {
                'user_info': st.session_state.user_info,
                'session_started': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat(),
                'total_assessments': 1,
                'assessments': [assessment_data]
            }
    else:
        all_data = {
            'user_info': st.session_state.user_info,
            'session_started': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat(),
            'total_assessments': 1,
            'assessments': [assessment_data]
        }
    
    try:
        with open(filepath, 'w') as f:
            json.dump(all_data, f, indent=4)
    except Exception as e:
        st.error(f"Error saving assessment data: {e}")
        return None
    
    return filepath

def prepare_assessment_data():
    return {
        "assessment_number": st.session_state.assessments_count + 1,
        "timestamp": datetime.now().isoformat(),
        "image_filename": os.path.basename(st.session_state.current_image_path),
        "ai_classification": st.session_state.current_label,
        "responses": st.session_state.responses
    }