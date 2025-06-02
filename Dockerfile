FROM nvidia/cuda:11.8.0-runtime-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependências
RUN apt-get update && apt-get install -y \
    python3 python3-pip ffmpeg git curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Atualizar pip
RUN python3 -m pip install --upgrade pip

# Instalar PyTorch com suporte CUDA
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Copiar código da aplicação
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ /app/app/
WORKDIR /app

# Rodar uvicorn apontando corretamente para app.main
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
