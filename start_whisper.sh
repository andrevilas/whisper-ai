#!/bin/bash

set -e

APP_IMAGE="whisper-api-gpu"
AUDIO_DIR="$(pwd)/audios"
CACHE_DIR="$HOME/.cache/whisper"
PORT=${1:-8000}

echo "🔍 Verificando se o Docker está instalado..."
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado. Por favor, instale o Docker."
    exit 1
fi
echo "✅ Docker instalado."

echo "🔍 Verificando se o driver NVIDIA está disponível..."
if ! command -v nvidia-smi &> /dev/null; then
    echo "❌ Driver NVIDIA não encontrado (nvidia-smi)."
    exit 2
fi
echo "✅ Driver NVIDIA OK."

echo "🔍 Verificando se o NVIDIA Container Toolkit está configurado..."
if ! docker info | grep -q 'Runtimes:.*nvidia'; then
    echo "❌ NVIDIA Container Toolkit não está configurado corretamente."
    echo "Siga: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html"
    exit 3
fi
echo "✅ NVIDIA Container Toolkit OK."

echo "🚀 Testando container de GPU..."
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu20.04 nvidia-smi > /dev/null || {
    echo "❌ Falha ao executar container com acesso à GPU."
    exit 4
}
echo "✅ Acesso à GPU confirmado dentro do container."

# Cria pastas de trabalho
mkdir -p "$AUDIO_DIR"
mkdir -p "$CACHE_DIR"

echo "📦 Verificando se a imagem '$APP_IMAGE' existe..."
if ! docker images | grep -q "$APP_IMAGE"; then
    echo "🔧 Imagem '$APP_IMAGE' não encontrada. Iniciando build automático..."
    docker build -t $APP_IMAGE .
fi
echo "✅ Imagem '$APP_IMAGE' pronta."

echo "🚀 Iniciando container da aplicação Whisper com GPU..."
docker run --rm --gpus all \
    -v "$AUDIO_DIR":/app/audios \
    -v "$CACHE_DIR":/root/.cache/whisper \
    -p $PORT:8000 \
    $APP_IMAGE
