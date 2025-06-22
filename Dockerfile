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
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY python_DNA/requirments.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

COPY python_DNA/ /app/
COPY *.py /app/ml_modules/
COPY *.txt /app/data/

RUN mkdir -p /app/media/images
RUN mkdir -p /app/staticfiles
RUN mkdir -p /app/ml_modules
RUN mkdir -p /app/data

RUN chmod -R 755 /app

RUN python manage.py collectstatic --noinput --clear || echo "Static files collection skipped"
RUN python manage.py migrate || echo "Migration skipped - will run at startup"

EXPOSE 8000

RUN echo '#!/bin/bash\necho "Starting Django application..."\npython manage.py migrate\npython manage.py runserver 0.0.0.0:8000' > /app/start.sh
RUN chmod +x /app/start.sh

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

CMD ["/app/start.sh"]
