import cv2
import os

def segment_image(input_path, output_folder):
    img = cv2.imread(input_path)

    # Sử dụng threshold để phân vùng ảnh
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, segmented_img = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY)

    # Lưu kết quả
    filename = os.path.basename(input_path)
    output_path = os.path.join(output_folder, f"segmented_{filename}")
    cv2.imwrite(output_path, segmented_img)

    return output_path
