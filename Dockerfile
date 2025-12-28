FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY data/ data/
COPY models/ models/

# Port configuration - can be overridden at build time
ARG API_PORT=8000
ENV API_PORT=${API_PORT}

EXPOSE ${API_PORT}

# Set python path to include src
ENV PYTHONPATH=/app/src

# Run the application
CMD ["sh", "-c", "uvicorn src.app:app --host 0.0.0.0 --port ${API_PORT}"]
