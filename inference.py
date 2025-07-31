from openai import OpenAI
from PIL import Image
import base64, io
from config import SYSTEM_PROMPT_TEMPLATE

client = OpenAI(api_key="0", base_url="https://2392f9cb450d.ngrok-free.app/v1")
MODEL_ID = "/midtier/paetzollab/scratch/chl4044/LLaMA-Factory/output/intern_vl_3-38b_lora_sft"


def _img_to_b64(img: Image.Image) -> str:
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()


def ask_question(image: Image.Image, question: str, classification: str | None = None) -> str:
    messages = []
    if classification:
        messages.append(
            {
                "role": "system",
                "content": SYSTEM_PROMPT_TEMPLATE.format(classification=classification),
            }
        )
    messages.append(
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{_img_to_b64(image)}"},
                },
                {"type": "text", "text": question},
            ],
        }
    )
    try:
        resp = client.chat.completions.create(
            model=MODEL_ID, messages=messages, temperature=0.2
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        fallback_msgs = []
        if classification:
            fallback_msgs.append(
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT_TEMPLATE.format(classification=classification),
                }
            )
        fallback_msgs.append(
            {
                "role": "user",
                "content": f"<image>{_img_to_b64(image)}</image>\n\n{question}",
            }
        )
        resp = client.chat.completions.create(
            model=MODEL_ID, messages=fallback_msgs, temperature=0.2
        )
        return resp.choices[0].message.content.strip()

def ask_question_stream(image: Image.Image, question: str, classification: str | None = None):
    messages = []
    if classification:
        messages.append(
            {
                "role": "system",
                "content": SYSTEM_PROMPT_TEMPLATE.format(classification=classification),
            }
        )
    messages.append(
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{_img_to_b64(image)}"},
                },
                {"type": "text", "text": question},
            ],
        }
    )
    stream = client.chat.completions.create(
        model=MODEL_ID, messages=messages, temperature=0.2, stream=True
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content


def generate_explanation(image: Image.Image, classification: str) -> str:
    prompt = (
        f"Generate a concise paragraph explaining why this OCTA image is classified as "
        f"{classification}. Focus on the specific regions that support this diagnosis."
    )
    return ask_question(image, prompt, classification)