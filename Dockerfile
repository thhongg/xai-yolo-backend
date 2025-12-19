# =====================================================
# Stage 1: Base (HEAVY – build once, cache lâu)
# =====================================================
FROM python:3.10-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# System deps
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

# ---- Torch CPU (ổn định cho Railway) ----
RUN pip install --no-cache-dir \
    torch==2.9.1 \
    ultralytics \
    grad-cam \
    opencv-python-headless

# Sanity check
RUN python - <<EOF
import torch
from pytorch_grad_cam import EigenCAM
print("Torch OK:", torch.__version__)
print("EigenCAM OK")
EOF


# =====================================================
# Stage 2: Runtime (APP + FASTAPI)
# =====================================================
FROM python:3.10-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Runtime system deps
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy Python env đã build
COPY --from=base /usr/local /usr/local

# ---- INSTALL FASTAPI STACK (QUAN TRỌNG) ----
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY app/ app/

EXPOSE 8080

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--log-level", "info"]