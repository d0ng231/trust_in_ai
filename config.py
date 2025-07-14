import os

OCTA_DIR = "./OCTA_500_bnry"
OUTPUT_DIR = "./results"

os.makedirs(OUTPUT_DIR, exist_ok=True)

LABELS = ["PDR", "NPDR", "Healthy"]

EXPLANATIONS = {
    "PDR": """This OCTA DCP image suggests a PDR (Proliferative Diabetic Retinopathy) condition. The extensive areas of capillary non-perfusion, characterized by large flow voids, are more severe and widespread compared to what would be expected in NPDR. Additionally, there are fine, tuft-like neovascularizations with brighter flow signals visible near the 7 o'clock position relative to the central FAZ, which is a hallmark of PDR but not typically seen in NPDR.""",
    
    "NPDR": """This OCTA DCP image indicates NPDR (Non-Proliferative Diabetic Retinopathy). The image shows moderate capillary dropout and irregular FAZ (foveal avascular zone) borders, with scattered microaneurysms visible as bright dots. The vascular changes are present but limited to the existing retinal vasculature without evidence of neovascularization. The capillary non-perfusion areas are smaller and less confluent compared to PDR.""",
    
    "Healthy": """This OCTA DCP image shows a healthy retinal vasculature pattern. The capillary network demonstrates uniform density with well-preserved flow throughout the macular region. The FAZ (foveal avascular zone) shows regular, smooth borders with appropriate size. There are no signs of capillary dropout, microaneurysms, or neovascularization. The vascular branching pattern appears normal with good perfusion in all quadrants."""
}

SPECIALTIES = ["Ophthalmology", "Retina Specialist", "General Practice", "Optometry", "Medical Student", "Other"]
EXPERIENCE_LEVELS = ["< 1 year", "1-5 years", "5-10 years", "10-20 years", "> 20 years"]
OCTA_EXPERIENCE = ["None", "Basic", "Intermediate", "Advanced", "Expert"]
AI_FAMILIARITY = ["Not familiar", "Somewhat familiar", "Moderately familiar", "Very familiar", "Expert"]