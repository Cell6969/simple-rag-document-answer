# Dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install
RUN apt-get update && apt-get install -y netcat-openbsd curl wget && rm -rf /var/lib/apt/lists/

# Install system dependencies (for sentence-transformers & PDF support)
RUN apt-get update && apt-get install -y \
    build-essential \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Install wait-for.sh
COPY wait-for.sh /wait-for.sh
COPY run.sh /run.sh
RUN chmod +x /wait-for.sh
RUN chmod +x /run.sh

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir "numpy<2.0" && \
    pip install --no-cache-dir torch==2.2.0+cpu --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# Run Flask app
CMD ["python", "app.py"]
