import whisper

# Cache de modelos carregados
_loaded_models = {}

def load_model(model_name="base"):
    if model_name not in _loaded_models:
        _loaded_models[model_name] = whisper.load_model(model_name, device="cuda")
    return _loaded_models[model_name]

def transcribe_audio(file_path, model_name="base", language="Portuguese"):
    model = load_model(model_name)
    result = model.transcribe(file_path, language=language)
    return result
