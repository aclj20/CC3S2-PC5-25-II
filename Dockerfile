# Imagen base slim 
FROM python:3.11-slim

# Variables generales 
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Instalar dependencias del sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Directorio de trabajo
WORKDIR /app

# Copiar dependencias primero
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar la aplicación
COPY . .

# Exponer puerto FastAPI
EXPOSE 8000

# HEALTHCHECK
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD \
    curl -f http://127.0.0.1:8000/health || exit 1

# Iniciar FastAPI con uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

