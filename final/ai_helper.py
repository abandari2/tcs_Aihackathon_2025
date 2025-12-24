import os
import base64
import cv2
import httpx 
from openai import OpenAI
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI 
from PIL import Image
import numpy as np

load_dotenv() 

client = OpenAI(
    api_key=os.environ["GENAILAB_API_KEY"],
    base_url="https://genailab.tcs.in",
    http_client=httpx.Client(verify=False)  # GenAILab needs this
)
import json
import re
import json

def parse_json_safe(content: str) -> dict:
    """
    Extract the first valid JSON object from the string,
    ignoring Markdown code blocks, backticks, or extra text.
    """
    # Remove ```json or ``` from the string
    content = re.sub(r'```(json)?', '', content, flags=re.IGNORECASE).strip()
    
    # Find the first {...} JSON object
    match = re.search(r'\{.*\}', content, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    return {"is_live": False, "reason": "AI response could not be parsed"}

def image_file_to_base64(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode("utf-8")


def openai_photo_liveness_check(base64_image: str) -> dict:
    """
    Returns:
    {
      "is_live": bool,
      "reason": str
    }
    """

    response = client.chat.completions.create(
        model="azure/genailab-maas-gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a bank-grade KYC liveness detection system. "
                    "Determine if the image is a REAL LIVE PERSON "
                    "or a PHOTO / SCREEN / PRINT / REPLAY ATTACK. "
                    "Always reply strictly in JSON."
                )
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Analyze the image and decide if it was captured live "
                            "by a webcam. Return JSON ONLY:\n"
                            "{ \"is_live\": true/false, \"reason\": \"short explanation\" }"
                        )
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        temperature=0,
        max_tokens=100
    )

    try:
        content = response.choices[0].message.content
        return parse_json_safe(content)
    except Exception:
        return {
            "is_live": False,
            "reason": "AI response could not be parsed"
        }



def has_face(image_file) -> bool:
    """
    Returns True if a face is detected in the uploaded image.
    """
    # Read image from Streamlit file or camera_input
    img = np.array(Image.open(image_file).convert("RGB"))

    # Convert to grayscale for face detection
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Load OpenCV pre-trained Haar cascade for frontal face
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    return len(faces)