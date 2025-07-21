import torch
from transformers import AutoProcessor, AutoModelForVision2Seq
from config import MODEL_PATH, DEVICE

processor = AutoProcessor.from_pretrained(MODEL_PATH)
model = AutoModelForVision2Seq.from_pretrained(MODEL_PATH).to(DEVICE)

def classify_and_explain(image):
    pixel_values = processor(images=image, return_tensors="pt").pixel_values.to(DEVICE)
    outputs = model.generate(pixel_values, max_new_tokens=4096)
    text = processor.decode(outputs[0], skip_special_tokens=True)
    parts = text.split("\n", 1)
    label = parts[0].strip()
    explanation = parts[1].strip() if len(parts) > 1 else ""
    return label, explanation

def ask_question(image, question):
    messages = [
        {
            "role": "user", 
            "content": [
                {"type": "image", "image": image},
                {"type": "text", "text": question}
            ]
        }
    ]
    
    text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    image_inputs, video_inputs = process_vision_info(messages)
    
    inputs = processor(
        text=[text],
        images=image_inputs,
        videos=video_inputs,
        padding=True,
        return_tensors="pt"
    ).to(DEVICE)
    
    with torch.no_grad():
        generated_ids = model.generate(**inputs, max_new_tokens=128)
    
    generated_ids_trimmed = [
        out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
    ]
    
    output_text = processor.batch_decode(
        generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
    )
    
    return output_text[0] if output_text else "No response generated."

def process_vision_info(conversations):
    image_inputs = []
    video_inputs = []
    for message in conversations:
        if isinstance(message["content"], list):
            for ele in message["content"]:
                if ele["type"] == "image":
                    image_inputs.append(ele["image"])
                elif ele["type"] == "video":
                    video_inputs.append(ele["video"])
    return image_inputs if image_inputs else None, video_inputs if video_inputs else None