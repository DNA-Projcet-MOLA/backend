# Use Python 3.11 slim image for better performance and smaller size
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Set work directory
WORKDIR /app

# Install system dependencies required for the project
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Required for pytesseract OCR
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-kor \
    # Required for OpenCV and image processing
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    # Required for building Python packages
    gcc \
    g++ \
    # Required for PostgreSQL (if needed)
    libpq-dev \
    # Git for installing packages from repositories
    git \
    # Cleanup
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY python_DNA/requirments.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project
COPY python_DNA/ /app/

# Copy the additional Python files (AI/ML modules)
COPY *.py /app/ml_modules/
COPY *.txt /app/data/ 2>/dev/null || true

# Create necessary directories
RUN mkdir -p /app/media/images
RUN mkdir -p /app/staticfiles
RUN mkdir -p /app/ml_modules
RUN mkdir -p /app/data

# Set proper permissions
RUN chmod -R 755 /app

# Collect static files
RUN python manage.py collectstatic --noinput --clear || echo "Static files collection skipped"

# Run database migrations
RUN python manage.py migrate || echo "Migration skipped - will run at startup"

# Expose port
EXPOSE 8000

# Create a startup script
RUN echo '#!/bin/bash\n\
echo "Starting Django application..."\n\
echo "Running migrations..."\n\
python manage.py migrate\n\
echo "Starting server..."\n\
python manage.py runserver 0.0.0.0:8000' > /app/start.sh

RUN chmod +x /app/start.sh

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Install curl for health check
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Default command
CMD ["/app/start.sh"]
