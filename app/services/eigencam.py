import torch
import torch.nn as nn
import numpy as np
import cv2
from pytorch_grad_cam import EigenCAM


class YOLOBackboneClassifier(nn.Module):
    """
    Adapter để biến YOLOv8 backbone thành classifier-style model
    (giống hệt cách bạn đã làm trong Colab)
    """

    def __init__(self, backbone: nn.Module):
        super().__init__()
        self.backbone = backbone
        self.pool = nn.AdaptiveAvgPool2d((1, 1))

    def forward(self, x):
        feats = self.backbone(x)          # [B, C, H, W]
        pooled = self.pool(feats)
        pooled = pooled.view(pooled.size(0), -1)
        return pooled                     # fake logits (EigenCAM chỉ cần feature)


def run_eigencam(
    yolo,
    target_layer,
    input_tensor,
    original_image
):
    """
    yolo          : YOLO object (ultralytics)
    target_layer  : backbone layer (vd: backbone[7])
    input_tensor  : torch.Tensor [1, 3, H, W]
    original_image: numpy image (H, W, 3)
    """

    device = next(yolo.model.parameters()).device
    input_tensor = input_tensor.to(device)

    # Lấy backbone YOLO
    backbone = yolo.model.model[:8]

    # Wrap backbone giống hệt Colab
    cam_model = YOLOBackboneClassifier(backbone).to(device)
    cam_model.eval()

    cam = EigenCAM(
        model=cam_model,
        target_layers=[cam_model.backbone[7]]
    )

    grayscale_cam = cam(input_tensor=input_tensor)[0]

    # Resize heatmap về kích thước ảnh gốc
    grayscale_cam = cv2.resize(
        grayscale_cam,
        (original_image.shape[1], original_image.shape[0])
    )

    heatmap = cv2.applyColorMap(
        np.uint8(255 * grayscale_cam),
        cv2.COLORMAP_JET
    )

    return heatmap
