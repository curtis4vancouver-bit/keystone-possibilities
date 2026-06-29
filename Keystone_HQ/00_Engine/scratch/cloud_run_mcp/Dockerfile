FROM python:3.11-slim

# Enforce clean stdout/stderr streaming
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy server code
COPY server.py .

# GCS FUSE mount point in Cloud Run
# Cloud Run automatically mounts to this path when configured in the deployment settings
RUN mkdir -p /gcs/brand-brain

EXPOSE 8080

CMD ["python", "server.py"]
