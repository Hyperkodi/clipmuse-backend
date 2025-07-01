import os
import subprocess
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import openai

app = FastAPI()

# Allow all CORS (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set your OpenAI API key from the environment
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/process")
async def process_video(file: UploadFile = File(...)):
    try:
        # Save uploaded file
        with open("input.mp4", "wb") as f:
            f.write(await file.read())

        # Extract audio to audio.wav
        subprocess.run(
            ["ffmpeg", "-i", "input.mp4", "-vn", "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "1", "audio.wav"],
            check=True
        )

        # Transcribe using OpenAI Whisper
        with open("audio.wav", "rb") as audio_file:
            transcript = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file
            )

        return JSONResponse(content={"transcript": transcript['text']})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
