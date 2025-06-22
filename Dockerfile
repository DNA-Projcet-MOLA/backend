FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# 필수 시스템 패키지 설치
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
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# torch는 CPU 전용으로 명시 설치 (pix2tex 등 호환을 위해)
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# requirements 설치
COPY python_DNA/requirments.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# 코드 복사
COPY python_DNA/ /app/
COPY *.py /app/ml_modules/
COPY *.txt /app/data/

# 폴더 생성 및 권한 설정
RUN mkdir -p /app/media/images /app/staticfiles /app/ml_modules /app/data \
    && chmod -R 755 /app

# 정적 파일 수집 및 마이그레이션 (실패해도 무시)
RUN python manage.py collectstatic --noinput --clear || true
RUN python manage.py migrate || true

# 실행 스크립트 등록
COPY --chmod=755 ./start.sh /app/start.sh

CMD ["/app/start.sh"]
