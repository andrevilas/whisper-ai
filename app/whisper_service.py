import whisper
import torch

# Cache de modelos carregados
_loaded_models = {}

def load_model(model_name="base"):
    if model_name not in _loaded_models:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        _loaded_models[model_name] = whisper.load_model(model_name, device=device)
    return _loaded_models[model_name]

def transcribe_audio(file_path, model_name="base", language="Portuguese"):
    model = load_model(model_name)
    result = model.transcribe(file_path, language=language)
    return result


def detect_language(file_path, model_name="base"):
    model = load_model(model_name)

    result = model.transcribe(file_path, language=None)

    return {
        "detected_language": result.get("language", "unknown"),
        "probabilities": result.get("language_probs", {})
    }

def smart_transcribe(file_path, model_name="base", language=None):
    model = load_model(model_name)

    if language is None:
        # Detecta idioma automaticamente
        audio = whisper.load_audio(file_path)
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio).to(model.device)
        _, probs = model.detect_language(mel)
        detected_language = max(probs, key=probs.get)
    else:
        detected_language = language.lower()

    result = model.transcribe(file_path, language=detected_language)

    return {
        "transcription": result["text"],
        "language_used": detected_language
    }
