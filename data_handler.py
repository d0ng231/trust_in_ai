import json
import os
from datetime import datetime
import streamlit as st
from config import OUTPUT_DIR

def save_assessment_to_json(assessment_data):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    user_name = st.session_state.user_info.get('name', 'unknown').replace(' ', '_')
    filename = f"{user_name}_assessments.json"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                content = f.read().strip()
                if content:
                    all_data = json.loads(content)
                else:
                    all_data = None
        except (json.JSONDecodeError, Exception) as e:
            st.warning(f"Existing file corrupted, creating new file: {e}")
            all_data = None
        
        if all_data:
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
    submission_time = datetime.now()
    time_spent = (
        (submission_time - st.session_state.case_start_time).total_seconds()
        if st.session_state.case_start_time
        else None
    )
    return {
        "assessment_number": st.session_state.assessments_count + 1,
        "timestamp": submission_time.isoformat(),
        "image_filename": os.path.basename(st.session_state.current_image_path),
        "ai_classification": st.session_state.current_label,
        "explanation_type": st.session_state.current_explanation_type,
        "time_spent_seconds": time_spent,
        "responses": st.session_state.responses,
        "chat_history": st.session_state.chat_history,
    }