import os
import torch

OCTA_DIR = "/midtier/paetzollab/scratch/chl4044/streamlit_ui_trust_in_ai/OCTA_500_bnry"
OUTPUT_DIR = "/midtier/paetzollab/scratch/chl4044/streamlit_ui_trust_in_ai/results"
ENTRIES_FILE = "metadata.json"
MODEL_PATH = "Qwen/Qwen2.5-VL-7B-Instruct"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
LABELS = ["PDR", "NPDR", "Healthy"]
SPECIALTIES = ["Ophthalmology", "Retina Specialist", "General Practice", "Optometry", "Medical Student", "Other"]
EXPERIENCE_LEVELS = ["< 1 year", "1-5 years", "5-10 years", "10-20 years", "> 20 years"]
OCTA_EXPERIENCE = ["None", "Basic", "Intermediate", "Advanced", "Expert"]
AI_FAMILIARITY = ["Not familiar", "Somewhat familiar", "Moderately familiar", "Very familiar", "Expert"]