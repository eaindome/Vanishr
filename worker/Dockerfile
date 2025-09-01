# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Set work directory
WORKDIR /worker

# Install system dependencies for playwright and weasyprint
RUN apt-get update && \
    apt-get install -y wget gnupg libpango-1.0-0 libgdk-pixbuf-2.0-0 libffi-dev libssl-dev libxml2 libxslt1.1 libjpeg-dev libpng-dev libpq-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

# Install Playwright dependencies
RUN pip install --upgrade pip && \
    pip install playwright && \
    playwright install --with-deps chromium

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy worker code
COPY . .

# Default command
CMD ["python", "worker.py"]
