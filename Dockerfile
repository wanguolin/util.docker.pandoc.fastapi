FROM python:3.9-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    pandoc \
    wkhtmltopdf \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir fastapi uvicorn python-multipart

WORKDIR /app
COPY app.py .

EXPOSE 8080
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
