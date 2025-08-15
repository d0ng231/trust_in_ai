import json
import os
import requests
import streamlit as st
from datetime import datetime
import base64
from PIL import Image
import io
from pathlib import Path
from config import (
    APPSCRIPT_URL, DRIVE_FOLDER_KEYS, ENTRIES_FILE, PASSWORD_FILE_NAME,
    LOCAL_METADATA_PATH, LOCAL_PASSWORD_PATH, LOCAL_IMAGE_DIR,
    LOCAL_OVERLAY_DIR, LOCAL_CSV_DIR, LOCAL_GRADCAM_DIR, LOCAL_RESULTS_DIR, LOCAL_DATA_DIR,
    GENERATE_LIVE_EXPLANATION
)

def _make_post_request(payload):
    try:
        r = requests.post(
            APPSCRIPT_URL,
            data=json.dumps(payload, ensure_ascii=False),
            headers={"Content-Type": "application/json"},
            timeout=120,
        )
        r.raise_for_status()
        response_json = r.json()
        if response_json.get("status") != "OK":
            raise RuntimeError(f"Server Error: {response_json.get('message')}")
        return response_json
    except requests.exceptions.RequestException as e:
        st.error(f"A connection error occurred during upload: {e}")
        raise e


def _fetch_raw_content(params):
    try:
        r = requests.get(APPSCRIPT_URL, params=params, timeout=30)
        r.raise_for_status()
        
        content_type = r.headers.get('content-type', '')

        # The server sends JSON only for status/error messages.
        # A successful file download is sent as plain text.
        if 'application/json' in content_type:
            json_content = r.json()
            if json_content.get('status') != 'OK':
                st.warning(f"Server reported an issue: {json_content.get('message', 'Unspecified error.')}")
                return None
            # If status is OK, it's likely from a 'list_files' call. Return the raw text for parsing.
            return r.text
        else:
            # Assumed to be a successful file download (text/plain)
            return r.text

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            # This is a normal "not found" case, not an error.
            return None
        st.error(f"A network error occurred: {e}")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"A connection error occurred: {e}")
        return None

def get_drive_file_by_name(filename, folder_key):
    return _fetch_raw_content({"filename": filename, "folderKey": folder_key})

def get_drive_file_by_id(file_id):
    return _fetch_raw_content({"fileId": file_id})

def list_drive_files(folder_key):
    params = {"action": "list_files", "folderKey": folder_key}
    content = _fetch_raw_content(params)
    if content:
        try:
            response_json = json.loads(content)
            if response_json.get("status") == "OK":
                return response_json.get("files", [])
        except json.JSONDecodeError:
            st.error("Failed to parse file list from server.")
            return []
    return []

def get_local_path(drive_path_str: str) -> Path | None:
    filename = os.path.basename(drive_path_str)
    if "DCP_images" in drive_path_str:
        return LOCAL_IMAGE_DIR / filename
    elif "DCP_overlay_cropped" in drive_path_str:
        return LOCAL_OVERLAY_DIR / filename
    elif "CSVs" in drive_path_str:
        return LOCAL_CSV_DIR / filename
    elif "CNN_gradcam" in drive_path_str:
        return LOCAL_GRADCAM_DIR / filename
    return None

def synchronize_drive_data():
    st.info("Initializing session (cold start).")
    progress_bar = st.progress(0, text="Fetching required data...")
    LOCAL_DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not LOCAL_METADATA_PATH.exists():
        content = get_drive_file_by_name(ENTRIES_FILE, DRIVE_FOLDER_KEYS["root_data"])
        if content:
            LOCAL_METADATA_PATH.write_text(content, encoding='utf-8')
    if not LOCAL_METADATA_PATH.exists():
        st.error("Fatal: Could not retrieve assessment data. Cannot proceed.")
        st.stop()
    entries = json.loads(LOCAL_METADATA_PATH.read_text(encoding='utf-8'))
    all_drive_paths = set()
    for entry in entries:
        if entry.get('image_id'):
            all_drive_paths.add(entry['image_id'])
        # Skip downloading pre-generated explanation assets if generating live explanations
        if (not GENERATE_LIVE_EXPLANATION) and entry.get('explanation_type') != 'text' and entry.get('explanation'):
            all_drive_paths.add(entry['explanation'])
        if entry.get('csv_path'):
            all_drive_paths.add(entry['csv_path'])
    missing_paths = [p for p in all_drive_paths if not (lp := get_local_path(p)) or not lp.exists()]
    if not missing_paths:
        progress_bar.empty()
        st.success("Initialization complete. Starting assessment.")
        return
    payload = {"action": "get_bulk", "paths": missing_paths}
    try:
        response = _make_post_request(payload)
        bulk_data = response.get("data", {})
        total_files = len(bulk_data)
        for i, (drive_path, b64_content) in enumerate(bulk_data.items()):
            local_path = get_local_path(drive_path)
            if local_path and b64_content:
                local_path.parent.mkdir(parents=True, exist_ok=True)
                progress_bar.progress(int((i + 1) / total_files * 100), text=f"Preparing asset {i+1} of {total_files}...")
                try:
                    decoded_content = base64.b64decode(b64_content)
                    local_path.write_bytes(decoded_content)
                except Exception as e:
                    st.warning(f"Could not prepare asset: {local_path.name}")
        progress_bar.empty()
        st.success("Initialization complete. Starting assessment.")
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")
        st.stop()

def synchronize_drive_results():
    st.info("Syncing results files...")
    results_folder_key = DRIVE_FOLDER_KEYS['results']
    file_list = list_drive_files(results_folder_key)
    if not file_list:
        st.warning("No results files found on the server.")
        return
    
    success_count = 0
    failure_count = 0
    
    for file_info in file_list:
        filename = file_info.get("name", "Unknown file")
        file_id = file_info.get("id")
        if not file_id:
            st.warning(f"Skipping a file entry with no ID: '{filename}'")
            failure_count += 1
            continue
        
        content = get_drive_file_by_id(file_id)
        
        if content:
            local_path = LOCAL_RESULTS_DIR / filename
            local_path.parent.mkdir(parents=True, exist_ok=True)
            local_path.write_text(content, encoding='utf-8')
            success_count += 1
        else:
            st.warning(f"Failed to download content for: {filename}")
            failure_count += 1

    if failure_count == 0 and success_count > 0:
        st.success(f"Successfully synchronized {success_count} result file(s).")
    elif success_count > 0 and failure_count > 0:
        st.error(f"Synchronization complete with errors. Downloaded {success_count} file(s), but failed on {failure_count} file(s).")
    else:
        st.error(f"Synchronization failed. Could not download any of the {len(file_list)} result file(s).")

def fetch_password_on_demand():
    return get_drive_file_by_name(PASSWORD_FILE_NAME, DRIVE_FOLDER_KEYS["root_data"])

def fetch_metadata():
    return json.loads(LOCAL_METADATA_PATH.read_text(encoding='utf-8')) if LOCAL_METADATA_PATH.exists() else None

def _get_current_local_assessment_path():
    LOCAL_RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    return LOCAL_RESULTS_DIR / f"{st.session_state.session_id}_assessments.json"

def append_assessment_locally(data):
    local_path = _get_current_local_assessment_path()
    doc = {}
    if local_path.exists():
        doc = json.loads(local_path.read_text(encoding='utf-8'))
    if "assessments" not in doc:
        doc["session_id"] = st.session_state.session_id
        doc["session_started"] = datetime.now().isoformat()
        doc["assessments"] = []
    doc["assessments"].append(data)
    doc["total_assessments"] = len(doc["assessments"])
    doc["last_updated"] = datetime.now().isoformat()
    local_path.write_text(json.dumps(doc, indent=2), encoding='utf-8')

def finalize_and_upload(user_info):
    temp_path = _get_current_local_assessment_path()
    if not temp_path.exists():
        st.error("Error: Could not find assessment data to finalize.")
        return
    doc = json.loads(temp_path.read_text(encoding='utf-8'))
    doc["user_info"] = user_info
    doc["last_updated"] = datetime.now().isoformat()
    user_name = user_info.get("name", st.session_state.session_id).replace(" ", "_")
    final_fname = f"{user_name}_assessments.json"
    final_path = LOCAL_RESULTS_DIR / final_fname
    final_path.parent.mkdir(parents=True, exist_ok=True)
    final_path.write_text(json.dumps(doc, indent=2), encoding='utf-8')
    payload = {"action": "save", "folderKey": DRIVE_FOLDER_KEYS["results"], "filename": final_fname, "data": doc}
    try:
        _make_post_request(payload)
        st.success("Your assessment has been securely submitted.")
        temp_path.unlink(missing_ok=True)
    except Exception as e:
        st.error("An error occurred during submission. Your responses have been saved. Please contact the study administrator.")

def prepare_assessment_data():
    t = datetime.now()
    spent = (t - st.session_state.case_start_time).total_seconds() if st.session_state.case_start_time else None
    return {
        "assessment_number": st.session_state.assessments_count + 1,
        "timestamp": t.isoformat(),
        "image_filename": os.path.basename(st.session_state.current_image_path),
        "ai_classification": st.session_state.current_label,
        "explanation_type": st.session_state.current_explanation_type,
        "time_spent_seconds": spent,
        "responses": st.session_state.responses,
        "chat_history": st.session_state.chat_history,
    }