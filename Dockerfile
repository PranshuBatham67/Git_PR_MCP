FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user and set up directory permissions
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app

# Switch to non-root user
USER app

# Copy requirements first (for better layer caching)
COPY --chown=app:app requirements.txt .

# Create virtual environment and install dependencies
RUN python -m venv /app/venv \
    && /app/venv/bin/pip install --upgrade pip \
    && /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=app:app . .

# Expose port
EXPOSE 8080

# Set environment variables for production
ENV HOST=0.0.0.0
ENV PORT=8080

# Run the webhook server using venv
CMD ["/app/venv/bin/python", "webhook_server.py"]
