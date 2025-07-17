import os

OCTA_DIR = "/midtier/paetzollab/scratch/chl4044/streamlit_ui_trust_in_ai/OCTA_500_bnry"
OUTPUT_DIR = "/midtier/paetzollab/scratch/chl4044/streamlit_ui_trust_in_ai/results"
ENTRIES_FILE = "/midtier/paetzollab/scratch/chl4044/streamlit_ui_trust_in_ai/metadata.json"

os.makedirs(OUTPUT_DIR, exist_ok=True)

LABELS = ["PDR", "NPDR", "Healthy"]

SPECIALTIES = ["Ophthalmology", "Retina Specialist", "General Practice", "Optometry", "Medical Student", "Other"]
EXPERIENCE_LEVELS = ["< 1 year", "1-5 years", "5-10 years", "10-20 years", "> 20 years"]
OCTA_EXPERIENCE = ["None", "Basic", "Intermediate", "Advanced", "Expert"]
AI_FAMILIARITY = ["Not familiar", "Somewhat familiar", "Moderately familiar", "Very familiar", "Expert"]
