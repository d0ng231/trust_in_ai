import os
import torch

OCTA_DIR = "data/DCP_images"
OUTPUT_DIR = "results"
ENTRIES_FILE = "metadata.json"
GENERATE_LIVE_EXPLANATION = False
EVALUATION_MODE = True
SYSTEM_PROMPT_TEMPLATE = (
    "You are an ophthalmology AI assistant. "
    "The OCTA image has been classified as **{classification}**. "
    "Stick to that classification and focus on specific regions of the image "
    "that support it."
)
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
LABELS = ["PDR", "NPDR", "Healthy"]
SPECIALTIES = ["Ophthalmology", "Retina Specialist", "General Practice", "Optometry", "Medical Student", "Other"]
EXPERIENCE_LEVELS = ["< 1 year", "1-5 years", "5-10 years", "10-20 years", "> 20 years"]
OCTA_EXPERIENCE = ["None", "Basic", "Intermediate", "Advanced", "Expert"]
AI_FAMILIARITY = ["Not familiar", "Somewhat familiar", "Moderately familiar", "Very familiar", "Expert"]