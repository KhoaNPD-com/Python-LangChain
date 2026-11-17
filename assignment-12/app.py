# pip install openai pillow requests pydantic

import os
import base64
import requests
from pydantic import BaseModel
from openai import OpenAI

# -----------------------------
# CONFIG
# -----------------------------
from dotenv import load_dotenv
load_dotenv()

# -------------------------------
#  OpenAI Configuration
# -------------------------------

client = OpenAI(
 api_key=os.getenv('OPENAI_GPT_4O_API_KEY'),
 base_url=os.getenv('OPENAI_ENDPOINT'),
)

# -------------------------------
#  Output Schema
# -------------------------------
class CloudResponse(BaseModel):
    result: str
    accuracy: float

# -------------------------------
#  Dummy Input Images (AUTO input)
# -------------------------------
image_urls = [
    # Cloudy
    "https://images.pexels.com/photos/53594/blue-clouds-day-fluffy-53594.jpeg",
    # Clear sky
    "https://images.pexels.com/photos/28466908/pexels-photo-28466908.jpeg",
    # Mixed clouds
    "https://images.pexels.com/photos/32049610/pexels-photo-32049610.jpeg"
]

# -------------------------------
#  Process Each Image
# -------------------------------
for idx, image_url in enumerate(image_urls):
    print(f"\n[INFO] Processing Image {idx+1}")

    try:
        # --- Download image ---
        response = requests.get(image_url)
        image_bytes = response.content
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        # --- Prompt ---
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an image classification model.\n"
                    "Classify satellite images into ONLY:\n"
                    "- 'Cloudy'\n"
                    "- 'Clear'\n"
                    "Also provide accuracy percentage.\n"
                    "Return JSON format: {\"result\": \"Cloudy or Clear\", \"accuracy\": 0-100}"
                )
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Classify this satellite image."},
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{image_base64}"
                    }
                ]
            }
        ]

        # --- Call OpenAI ---
        completion = client.chat.completions.create(
            model=os.getenv('OPENAI_MODEL_GPT_4O'),
            messages=messages,
            temperature=0
        )

        raw_output = completion.choices[0].message.content

        print("[DEBUG] Raw model output:", raw_output)

        # --- Parse Output ---
        parsed = CloudResponse.model_validate_json(raw_output)

        print(f"[RESULT] Prediction: {parsed.result}")
        print(f"[RESULT] Accuracy: {parsed.accuracy}%")

    except Exception as e:
        print(f"[ERROR] Failed on image {idx+1}: {e}")
