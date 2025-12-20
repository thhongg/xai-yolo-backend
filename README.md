# Hostname
https://xai-yolo-backend.fly.dev
# sample request
curl -X POST https://xai-yolo-backend.fly.dev/infer ^
-F "file=<@your_dir>:\<your_image>.jpg" 
# xai-yolo-backend

Backend inference service for **YOLOv8m** with **EigenCAM (Explainable AI)**.

This repository contains **source code only**.  
Model artifacts (`.pt`, `.onnx`) are **NOT committed**, in compliance with **12-Factor App principles** and standard MLOps practices.

---

## 1. Overview

### Features
- Object detection using **YOLOv8m**
- Explainable AI visualization using **EigenCAM**
- Stateless **REST API** backend

### Design Principles
- Stateless backend
- Externalized configuration via environment variables
- Model artifacts managed outside Git
- Ultralytics Hub as Model Registry

---

## 2. Requirements

### Option A (Recommended): Docker
- Docker >= 20.x
- Docker Compose

### Option B: Local Python
- Python >= 3.10
- pip

---

## 3. Repository Structure


```
.
├── app/
│ ├── api/ # API endpoints
│ ├── core/ # Pre/Post processing
│ ├── services/ # Model loading, XAI, visualization
│ ├── config.py
│ └── main.py
├── models/ # Model directory (NOT tracked by Git)
├── Dockerfile
├── Dockerfile.base
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

## 4. Model Setup (Required)

⚠️ **Model file is NOT included in this repository.**

The YOLOv8m model is trained and hosted on **Ultralytics Hub**, which acts as a **Model Registry** (similar to HuggingFace Hub or MLflow Registry).
The backend expects a YOLOv8-compatible PyTorch model, either loaded locally
or resolved via Ultralytics Hub.

## 4.1. Model Registry (Ultralytics Hub)

The trained YOLOv8m model is publicly available on **Ultralytics Hub**:

Model URL:
https://hub.ultralytics.com/models/QfV3QWptr2E9CldzLQCr

This Hub model acts as the **single source of truth** for:
- Model versioning
- Model sharing
- Reproducibility

---
### Optional: Load model directly from Ultralytics Hub

Instead of downloading the `.pt` file manually, the model can be loaded
directly from Ultralytics Hub:

```python
from ultralytics import YOLO

model = YOLO("https://hub.ultralytics.com/models/QfV3QWptr2E9CldzLQCr")
```

### 4.2. Place model locally

From the project root:

```
mkdir -p models
cp /path/to/model.pt models/model.pt
```
Expected path:
models/model.pt

### 5. Configuration

Copy environment variables template:

```
cp .env.example .env
```

### 6. Run with Docker (Recommended)

```
docker compose up --build
```

Service available at:

```
http://localhost:8000
```

### 7. Run Locally (Without Docker)

```
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app/main.py
```

### 8. API Example

```
curl -X POST http://localhost:8000/infer \
  -F "file=@image.jpg"
```
The response includes:
- Bounding boxes
- Class labels
- Confidence scores
- EigenCAM heatmap visualization

