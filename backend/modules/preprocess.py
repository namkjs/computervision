import cv2
import os
from modules.read import read_image  # Import hàm từ file read.py

def gray(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray_img

