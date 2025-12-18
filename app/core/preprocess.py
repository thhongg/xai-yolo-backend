import cv2
import torch
import numpy as np


def preprocess_image(image_path, img_size=640):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    resized = cv2.resize(image_rgb, (img_size, img_size))
    tensor = torch.from_numpy(resized).float() / 255.0
    tensor = tensor.permute(2, 0, 1).unsqueeze(0)

    return image, tensor
