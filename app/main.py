from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import PlainTextResponse, JSONResponse
import tempfile
import shutil
from app.whisper_service import transcribe_audio, detect_language, smart_transcribe
from app.enums import WhisperModel, SupportedLanguage
from typing import Optional

app = FastAPI()

@app.post("/transcribe", response_class=PlainTextResponse)
async def transcribe(
    audio_file: UploadFile = File(...),
    model: WhisperModel = Form(WhisperModel.base),
    language: SupportedLanguage = Form(SupportedLanguage.portuguese)
):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        shutil.copyfileobj(audio_file.file, tmp)
        tmp_path = tmp.name

    result = transcribe_audio(
        tmp_path,
        model_name=model.value,
        language=language.value
    )
    return result["text"]



from typing import Optional
from app.enums import WhisperModel, SupportedLanguage

@app.post("/transcribe/segments", response_class=JSONResponse)
async def transcribe_with_segments(
    audio_file: UploadFile = File(...),
    model: WhisperModel = Form(WhisperModel.base),
    language: SupportedLanguage = Form(SupportedLanguage.portuguese),
):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        shutil.copyfileobj(audio_file.file, tmp)
        tmp_path = tmp.name

    result = transcribe_audio(
        tmp_path,
        model_name=model.value,
        language=language.value
    )
    segments = [
        {"start": s["start"], "end": s["end"], "text": s["text"]}
        for s in result.get("segments", [])
    ]
    return segments

@app.post("/detect-language", response_class=JSONResponse)
async def detect_language_endpoint(
    audio_file: UploadFile = File(...),
    model: WhisperModel = Form(WhisperModel.base)
):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        shutil.copyfileobj(audio_file.file, tmp)
        tmp_path = tmp.name

    result = detect_language(tmp_path, model_name=model.value)
    return result

@app.post("/smart-transcribe", response_class=JSONResponse)
async def smart_transcribe_endpoint(
    audio_file: UploadFile = File(...),
    model: WhisperModel = Form(WhisperModel.base),
    language: Optional[SupportedLanguage] = Form(None)
):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        shutil.copyfileobj(audio_file.file, tmp)
        tmp_path = tmp.name

    result = smart_transcribe(
        tmp_path,
        model_name=model.value,
        language=language.value if language else None
    )
    return result
