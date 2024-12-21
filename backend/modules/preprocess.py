import cv2
import os
from read import read_image  # Import hàm từ file read.py

def preprocess_image(input_path):
    img = read_image(input_path)
    gray_img = cv2.cvtColor(img["image_data"], cv2.COLOR_BGR2GRAY)
    output_path = os.path.join(output_folder, f"preprocessed_{img['filename']}")
    cv2.imwrite(output_path, gray_img)
    return gray_img

input_path = "static/uploads/input.png"
output_folder = "static/results"


processed_image = preprocess_image(
    input_path
)