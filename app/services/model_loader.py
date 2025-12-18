import torch
from ultralytics import YOLO

# Singleton-style loader (12-factor: load once)
_yolo_model = None
_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def load_model(model_path: str):
    global _yolo_model

    if _yolo_model is None:
        yolo = YOLO(model_path)
        yolo.model.to(_device)
        yolo.model.eval()
        _yolo_model = yolo

    return _yolo_model


def get_device():
    return _device


def get_eigencam_target_layer(yolo):
    """
    Target layer chuẩn cho YOLOv8m:
    - Layer cuối backbone (C2f)
    - Phù hợp EigenCAM (feature-rich, spatial)
    """
    # YOLOv8 backbone thường nằm ở model.model[:8]
    return yolo.model.model[7]
