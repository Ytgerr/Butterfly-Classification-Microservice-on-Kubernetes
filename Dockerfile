# Use explicit Python version
FROM python:3.11-slim

# Create and switch to a non-root user
RUN useradd -m appuser && \
    mkdir -p /app && \
    chown appuser:appuser /app
WORKDIR /app
USER appuser

# Install dependencies first (better layer caching)
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=appuser:appuser model/ ./model
COPY --chown=appuser:appuser src/ ./src

# Use environment variable for port
ENV PORT=2005
EXPOSE $PORT

# Use exec form for CMD
CMD ["python", "src/server.py"]
