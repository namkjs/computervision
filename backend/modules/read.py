import cv2
import os

def read_image(input_path):
    # Đọc ảnh
    img = cv2.imread(input_path)
    if img is None:
        raise FileNotFoundError(f"Image at {input_path} not found or cannot be read.")

    filename = os.path.basename(input_path)
    resolution = img.shape[:2]
    total_pixels = img.size
    data_type = img.dtype
    dimension = img.ndim

    img = {
        "filename": filename,
        "resolution": resolution,
        "total_pixels": total_pixels,
        "data_type": str(data_type),
        "dimension": dimension,
        "image_data": img,  
    }

    return img

# input_path = "static/uploads/input.png"
# image_info = read_image(input_path)
# print(image_info)
# print("Image Info:", image_info)
