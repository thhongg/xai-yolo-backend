import cv2
import numpy as np


def draw_detections(image, detections):
    img = image.copy()

    for det in detections:
        x1, y1, x2, y2 = map(int, det["bbox"])
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

    return img


def overlay_heatmap(image, heatmap, alpha=0.5):
    return cv2.addWeighted(image, 1 - alpha, heatmap, alpha, 0)
