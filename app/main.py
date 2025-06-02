from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import PlainTextResponse, JSONResponse
import tempfile
import shutil
from app.whisper_service import transcribe_audio, detect_language, smart_transcribe

app = FastAPI()

@app.post("/transcribe", response_class=PlainTextResponse)
async def transcribe(
    audio_file: UploadFile = File(...),
    model: str = Form("base"),
    language: str = Form("Portuguese"),
):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        shutil.copyfileobj(audio_file.file, tmp)
        tmp_path = tmp.name

    result = transcribe_audio(tmp_path, model_name=model, language=language)
    return result["text"]


@app.post("/transcribe/segments", response_class=JSONResponse)
async def transcribe_with_segments(
    audio_file: UploadFile = File(...),
    model: str = Form("base"),
    language: str = Form("Portuguese"),
):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        shutil.copyfileobj(audio_file.file, tmp)
        tmp_path = tmp.name

    result = transcribe_audio(tmp_path, model_name=model, language=language)
    segments = [
        {"start": s["start"], "end": s["end"], "text": s["text"]}
        for s in result.get("segments", [])
    ]
    return segments

@app.post("/detect-language", response_class=JSONResponse)
async def detect_language_endpoint(
    audio_file: UploadFile = File(...),
    model: str = Form("base")
):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        shutil.copyfileobj(audio_file.file, tmp)
        tmp_path = tmp.name

    result = detect_language(tmp_path, model_name=model)
    return result

@app.post("/smart-transcribe", response_class=JSONResponse)
async def smart_transcribe_endpoint(
    audio_file: UploadFile = File(...),
    model: str = Form("base"),
    language: str = Form(None)  # Pode ser null
):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        shutil.copyfileobj(audio_file.file, tmp)
        tmp_path = tmp.name

    result = smart_transcribe(tmp_path, model_name=model, language=language)
    return result