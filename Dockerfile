# Dockerfile for PDF Outline Extraction
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY main.py .

# Create directories for input/output
RUN mkdir -p /app/input /app/output

# Set entrypoint
ENTRYPOINT ["python", "main.py"]