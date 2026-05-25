# Use a imagem oficial do Python leve
FROM python:3.11-slim

# Defina o diretório de trabalho no container
WORKDIR /app

# Instale dependências do sistema para o build e compilação do ChromaDB
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copie apenas o arquivo de requisitos primeiro (aproveita cache do Docker)
COPY requirements.txt .

# Instale as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie todo o projeto para dentro do container
COPY . .

# Variáveis de Ambiente Padrão
ENV PYTHONPATH=/app
ENV HOST=0.0.0.0
ENV PORT=8000

# Exponha a porta que o FastAPI usará
EXPOSE 8000

# Comando para iniciar o servidor (SaveinCloud mapeará a porta exposta)
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
