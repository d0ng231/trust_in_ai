import os
import torch

OCTA_DIR = "/midtier/paetzollab/scratch/chl4044/streamlit_ui_trust_in_ai/OCTA_500_bnry"
OUTPUT_DIR = "/midtier/paetzollab/scratch/chl4044/streamlit_ui_trust_in_ai/results"
ENTRIES_FILE = "metadata.json"
GENERATE_LIVE_EXPLANATION = False  
SYSTEM_PROMPT_TEMPLATE = (
    "You are an ophthalmology AI assistant. "
    "The OCT‑A image has been classified as **{classification}**. "
    "Stick to that classification and focus on specific regions of the image "
    "that support it."
)
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
LABELS = ["PDR", "NPDR", "Healthy"]
SPECIALTIES = ["Ophthalmology", "Retina Specialist", "General Practice", "Optometry", "Medical Student", "Other"]
EXPERIENCE_LEVELS = ["< 1 year", "1-5 years", "5-10 years", "10-20 years", "> 20 years"]
OCTA_EXPERIENCE = ["None", "Basic", "Intermediate", "Advanced", "Expert"]
AI_FAMILIARITY = ["Not familiar", "Somewhat familiar", "Moderately familiar", "Very familiar", "Expert"]