import cv2
import os
from modules.read import read_image  # Import hàm từ file read.py

def gray(input_path):
    img = read_image(input_path)
    gray_img = cv2.cvtColor(img["image_data"], cv2.COLOR_BGR2GRAY)
    return gray_img

