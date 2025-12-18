import numpy as np


def run_detection(yolo, image):
    """
    image: numpy array (BGR hoặc RGB đều được, YOLO tự xử lý)
    """
    results = yolo(image, verbose=False)

    detections = []

    for r in results:
        if r.boxes is None:
            continue

        boxes = r.boxes.xyxy.cpu().numpy()
        scores = r.boxes.conf.cpu().numpy()
        classes = r.boxes.cls.cpu().numpy()

        for box, score, cls in zip(boxes, scores, classes):
            detections.append({
                "bbox": box.tolist(),
                "confidence": float(score),
                "class_id": int(cls)
            })

    return detections, results
