import cv2
import numpy as np


# Chuyển đổi từ RGB sang YCbCr
def rgb_to_ycbcr(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)


# Chuyển đổi từ YCbCr sang RGB
def ycbcr_to_rgb(image):
    return cv2.cvtColor(image, cv2.COLOR_YCrCb2BGR)


# Chuyển đổi từ RGB sang HSV
def rgb_to_hsv(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


# Chuyển đổi từ HSV sang RGB
def hsv_to_rgb(image):
    return cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
