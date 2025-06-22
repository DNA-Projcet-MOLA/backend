FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-kor \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    gcc \
    g++ \
    libpq-dev \
    git \
    libgl1 \
    curl \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN curl https://sh.rustup.rs -sSf | sh -s -- -y \
    && . "$HOME/.cargo/env"

RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

COPY python_DNA/requirments.txt /app/requirements.txt
RUN pip install --upgrade pip setuptools wheel \
    && . "$HOME/.cargo/env" \
    && pip install --no-cache-dir -r requirements.txt

COPY python_DNA/ /app/
COPY *.py /app/ml_modules/
COPY *.txt /app/data/

RUN mkdir -p /app/media/images /app/staticfiles /app/ml_modules /app/data \
    && chmod -R 755 /app

RUN python manage.py collectstatic --noinput --clear || true
RUN python manage.py migrate || true

RUN echo '#!/bin/bash\n\
echo "Starting Django application..."\n\
python manage.py migrate\n\
python manage.py runserver 0.0.0.0:8000' > /app/start.sh \
    && chmod +x /app/start.sh

CMD ["/app/start.sh"]
