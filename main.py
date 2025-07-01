from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import uuid
import os

from transcribe import transcribe_audio
from select_clip import select_best_clip
from edit_video import cut_video
from generate_captions import add_captions

app = FastAPI()

@app.post("/process")
async def process_video(file: UploadFile = File(...)):
    input_filename = f"input_{uuid.uuid4()}.mp4"
    with open(input_filename, "wb") as f:
        f.write(await file.read())

    audio_path = "audio.wav"
    os.system(f"ffmpeg -y -i {input_filename} -vn -acodec pcm_s16le -ar 16000 -ac 1 {audio_path}")

    transcript = transcribe_audio(audio_path)
    start_time = select_best_clip(transcript)
    clip_path = "clip.mp4"
    cut_video(input_filename, start_time, 30, clip_path)

    captioned_path = "final_output.mp4"
    add_captions(clip_path, transcript, start_time, 30, captioned_path)

    return FileResponse(captioned_path, media_type="video/mp4", filename="clipmuse_result.mp4")
