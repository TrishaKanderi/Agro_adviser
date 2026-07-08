import base64
from sarvamai import SarvamAI
import os
from dotenv import load_dotenv

load_dotenv("agro_app.env") # This loads the variables from .env

API_KEY = os.getenv("SARVAM_API_KEY")
sarvam_client = SarvamAI(api_subscription_key=API_KEY)

def generate_tts_audio_base64(text: str, lang_code: str):
    response = sarvam_client.text_to_speech.convert(
        text=text,
        target_language_code=lang_code,
        model="bulbul:v3",
        pace=0.85,
        speaker="ratan"
    )
    # Just return the first string from the list
    if response.audios and len(response.audios) > 0:
        return response.audios[0]
    return None