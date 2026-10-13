# 1. Base Image: Usamos a versão slim oficial do Python 3.11 para uma imagem leve
FROM python:3.11-slim

# 2. Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    WORKDIR=/app \
    VIRTUAL_ENV=/opt/venv

# 3. Set working directory inside the container
WORKDIR ${WORKDIR}

# 4. Install system dependencies if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 5. Create the virtual environment and put it first on PATH
RUN python -m venv ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

# 6. Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

# 7. Install Python dependencies inside the virtual environment
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 8. Copy the rest of the application code
COPY . .

# 9. Expose FastAPI default port
EXPOSE 8000

# 10. Healthcheck to ensure container stability
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 11. Run FastAPI server using Uvicorn from the virtual environment
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]