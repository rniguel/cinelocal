# ==============================================================================
# CineLocal - Dockerfile Multi-Arch (HomeLabs, NAS e Servidores Linux)
# ==============================================================================
FROM python:3.11-slim

# Metadados
LABEL maintainer="CineLocal"
LABEL description="CineLocal - Central de Streaming Doméstico Estilo Netflix"

# Evita geração de .pyc e bufferiza logs do terminal
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    TZ=America/Sao_Paulo

# Instala FFmpeg e dependências essenciais do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    tzdata \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Cria diretório de trabalho
WORKDIR /cinelocal

# Copia os arquivos da aplicação
COPY app/ ./app/
COPY run.py ./
COPY media/ ./media/

# Cria pasta de dados para persistência se não existir
RUN mkdir -p /cinelocal/app/data

# Porta padrão de streaming e controle remoto
EXPOSE 8000

# Verificação de saúde da aplicação
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/status || exit 1

# Comando de inicialização
WORKDIR /cinelocal/app
CMD ["python", "servidor.py"]
