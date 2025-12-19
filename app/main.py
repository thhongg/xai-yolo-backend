from fastapi import FastAPI, UploadFile, File
import cv2
import uuid

from app.services.storage import upload_image
from app.services.model_loader import get_model, get_eigencam_target_layer
from app.services.detector import run_detection
from app.services.eigencam import run_eigencam
from app.services.visualizer import draw_detections, overlay_heatmap
from app.core.preprocess import preprocess_image

app = FastAPI(title="XAI YOLOv8 Backend")

# ❌ KHÔNG preload model trong startup


@app.post("/infer")
async def infer(file: UploadFile = File(...)):
    inference_id = str(uuid.uuid4())

    # ---- 1. Save input (ephemeral FS) ----
    tmp_input_path = f"/tmp/{inference_id}_input.jpg"
    with open(tmp_input_path, "wb") as f:
        f.write(await file.read())

    original_image, input_tensor = preprocess_image(tmp_input_path)

    # ---- 2. Detection ----
    model = get_model()
    target_layer = get_eigencam_target_layer(model)

    detections, results = run_detection(model, original_image)

    # ---- 3. EigenCAM ----
    heatmap = run_eigencam(
        model,
        target_layer,
        input_tensor,
        original_image
    )

    detect_img = draw_detections(original_image, detections)
    overlay_img = overlay_heatmap(detect_img, heatmap)

    # ---- 4. Save temp outputs ----
    tmp_detect = f"/tmp/{inference_id}_detect.jpg"
    tmp_heatmap = f"/tmp/{inference_id}_heatmap.jpg"
    tmp_overlay = f"/tmp/{inference_id}_overlay.jpg"

    cv2.imwrite(tmp_detect, detect_img)
    cv2.imwrite(tmp_heatmap, heatmap)
    cv2.imwrite(tmp_overlay, overlay_img)

    # ---- 5. Upload to MinIO ----
    detect_url = upload_image(tmp_detect, f"{inference_id}/detect.jpg")
    heatmap_url = upload_image(tmp_heatmap, f"{inference_id}/heatmap.jpg")
    overlay_url = upload_image(tmp_overlay, f"{inference_id}/overlay.jpg")

    return {
        "inference_id": inference_id,
        "detections": detections,
        "artifacts": {
            "detect": detect_url,
            "heatmap": heatmap_url,
            "overlay": overlay_url
        }
    }

@app.get("/health")
def health():
    return {"status": "ok"}
