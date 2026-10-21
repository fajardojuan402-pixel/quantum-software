FROM python:3.12-slim

WORKDIR /app

# Install system dependencies if needed (none for pure Python + Qiskit wheels)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app:/app/src

COPY . .

# Default command: run demo to verify installation
CMD ["python", "-m", "quantum_lab.demo"]
