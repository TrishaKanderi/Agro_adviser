import io
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

#imports from agroAdviser application
from utility_files.utils import preprocess_image
from agro_adviser_model.predictor import predict_disease
from TTSService.tts_service import generate_tts_audio_base64


app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"], # Allow your local HTML file to talk to the API
    allow_methods=["*"],
    allow_headers=["*"],
)

LANG_MAP = {
    "en": "en-IN",
    "te": "te-IN",
    "hi": "hi-IN"
}

@app.get("/")
def home():
    return {"message": "Agro Adviser API running"}

@app.post("/predict")
async def predict(file: UploadFile = File(...),lang: str="en"):
    image_bytes = await file.read()
    img = preprocess_image(image_bytes)
    result = predict_disease(img,lang)
    return result

@app.post("/tts")
async def tts_endpoint(text: str, lang: str = "en"):
    lang_code = LANG_MAP.get(lang, "en-IN")
    base64_audio = generate_tts_audio_base64(text, lang_code)

    if not base64_audio:
        return {"success": False, "error": "No audio generated"}

    return {
        "success": True,
        "audio_data": base64_audio, # This is the raw Base64 string
        "format": "wav"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)