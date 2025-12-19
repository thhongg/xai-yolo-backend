FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ----------------------------------------------------
# System dependencies (tối thiểu cho OpenCV)
# ----------------------------------------------------
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ----------------------------------------------------
# Upgrade pip
# ----------------------------------------------------
RUN pip install --upgrade pip

# ----------------------------------------------------
# Torch CPU ONLY (KHÓA – không cho pip upgrade)
# ----------------------------------------------------
RUN pip install --no-cache-dir \
    torch==2.2.2+cpu \
    torchvision==0.17.2+cpu \
    --index-url https://download.pytorch.org/whl/cpu


# ----------------------------------------------------
# Ultralytics MINIMAL deps (cài tay)
# ----------------------------------------------------
RUN pip install --no-cache-dir \
    psutil \
    pyyaml \
    tqdm \
    matplotlib \
    seaborn \
    requests

# ----------------------------------------------------
# ML libs (KHÔNG deps → KHÔNG torchvision)
# ----------------------------------------------------
# Ultralytics – khóa deps
RUN pip install --no-cache-dir \
    ultralytics==8.2.* \
    --no-deps

# XAI stack – cho phép deps tự resolve
RUN pip install --no-cache-dir \
    grad-cam \
    opencv-python-headless

# ----------------------------------------------------
# App-level dependencies
# ----------------------------------------------------
RUN pip install --no-cache-dir \
    fastapi==0.115.0 \
    uvicorn==0.38.0 \
    python-multipart==0.0.20 \
    python-dotenv>=1.0.1 \
    numpy==1.26.4 \
    Pillow>=10.0 \
    boto3>=1.34.0 \
    huggingface_hub>=0.22.0


# ----------------------------------------------------
# Copy source code
# ----------------------------------------------------
COPY app/ app/

EXPOSE 8080

# ----------------------------------------------------
# Start FastAPI
# ----------------------------------------------------
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]