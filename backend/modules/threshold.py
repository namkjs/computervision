import cv2
import numpy as np


# Ngưỡng hóa tĩnh (Global Thresholding)
def global_threshold(image, threshold=127):
    _, thresh_image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
    return thresh_image


# Ngưỡng hóa Otsu (Otsu's Thresholding)
def otsu_threshold(image):
    _, thresh_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh_image


# Ngưỡng hóa thích nghi (Adaptive Thresholding)
def adaptive_threshold(image, block_size=11, C=2):
    thresh_image = cv2.adaptiveThreshold(
        image,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        block_size,
        C,
    )
    return thresh_image
