FROM nvidia/cuda:11.8.0-runtime-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    python3 python3-pip ffmpeg git curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Atualizar pip
RUN python3 -m pip install --upgrade pip

# Instalar PyTorch com suporte a CUDA 11.8
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Copiar dependências Python e instalar
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiar código da aplicação
COPY app/ /app/app/
WORKDIR /app

# Copiar script de preload e rodar (para baixar os modelos)
COPY app/preload_models.py .
RUN python3 preload_models.py

# Expor a porta e iniciar o servidor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
