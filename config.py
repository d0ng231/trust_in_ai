import os
import torch
from pathlib import Path

LOCAL_DATA_DIR = Path("local_data")
LOCAL_METADATA_PATH = LOCAL_DATA_DIR / "metadata.json"
LOCAL_PASSWORD_PATH = LOCAL_DATA_DIR / "password.txt"
LOCAL_IMAGE_DIR = LOCAL_DATA_DIR / "images"
LOCAL_OVERLAY_DIR = LOCAL_DATA_DIR / "overlays"
LOCAL_CSV_DIR = LOCAL_DATA_DIR / "csvs"
LOCAL_GRADCAM_DIR = LOCAL_DATA_DIR / "gradcam"
LOCAL_RESULTS_DIR = LOCAL_DATA_DIR / "results"

APPSCRIPT_URL = "https://script.google.com/macros/s/AKfycbzTBlHlapAuWTYCTnsmJ1fr0a5Kov_RMbm6x8WT_MHlDzsOsbU3CCzOlh5pOLsWyF1M/exec"
ENTRIES_FILE = "metadata.json"
PASSWORD_FILE_NAME = "password.txt"

DRIVE_FOLDER_KEYS = {
    "root_data": "data",
    "images": "images",
    "overlays": "overlays",
    "csvs": "csvs",
    "gradcam": "gradcam",
    "results": "results"
}

GENERATE_LIVE_EXPLANATION = False
EVALUATION_MODE = False
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

LABELS = ["PDR", "NPDR", "Healthy"]
SPECIALTIES = ["Ophthalmology", "Retina Specialist", "General Practice", "Optometry", "Medical Student", "Other"]
EXPERIENCE_LEVELS = ["< 1 year", "1-5 years", "5-10 years", "10-20 years", "> 20 years"]
OCTA_EXPERIENCE = ["None", "Basic", "Intermediate", "Advanced", "Expert"]
AI_FAMILIARITY = ["Not familiar", "Somewhat familiar", "Moderately familiar", "Very familiar", "Expert"]

SYSTEM_PROMPT_TEMPLATE = (
    "You are an ophthalmology AI assistant. "
    "The OCTA image has been classified as **{classification}**. "
    "Stick to that classification and focus on specific regions of the image "
    "that support it."
)

for path in [LOCAL_DATA_DIR, LOCAL_IMAGE_DIR, LOCAL_OVERLAY_DIR, LOCAL_CSV_DIR, LOCAL_GRADCAM_DIR, LOCAL_RESULTS_DIR]:
    path.mkdir(parents=True, exist_ok=True)