import whisper
import os

MODELS = ["tiny", "base", "small", "medium", "large"]
CACHE_DIR = os.path.expanduser("~/.cache/whisper")

def is_model_cached(model_name: str) -> bool:
    model_path = os.path.join(CACHE_DIR, f"{model_name}.pt")
    return os.path.exists(model_path)

def main():
    for model in MODELS:
        if is_model_cached(model):
            print(f"✅ Modelo '{model}' já está presente no cache.")
        else:
            print(f"📦 Baixando modelo: {model}")
            whisper.load_model(model)

if __name__ == "__main__":
    main()
