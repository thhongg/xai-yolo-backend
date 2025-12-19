import os
from huggingface_hub import hf_hub_download
from ultralytics import YOLO

_model = None
_target_layer = None

def get_model():
    global _model
    if _model is not None:
        return _model

    repo_id = os.getenv("MODEL_REPO")
    filename = os.getenv("MODEL_FILE", "model.pt")
    model_dir = os.getenv("MODEL_DIR", "/app/models")

    if not repo_id:
        raise RuntimeError("MODEL_REPO env variable is not set")

    os.makedirs(model_dir, exist_ok=True)

    model_path = hf_hub_download(
        repo_id=repo_id,
        filename=filename,
        local_dir=model_dir,
        local_dir_use_symlinks=False
    )

    _model = YOLO(model_path)
    return _model


def get_eigencam_target_layer(model):
    """
    Return backbone layer for EigenCAM (YOLOv8m).
    """
    global _target_layer
    if _target_layer is not None:
        return _target_layer

    # YOLOv8 backbone: model.model.model[:8]
    _target_layer = model.model.model[7]
    return _target_layer
