import cv2
import os

def enhance_image(input_path, output_folder):
    img = cv2.imread(input_path)

    # Cải thiện ảnh bằng histogram equalization
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    enhanced_img = cv2.equalizeHist(gray_img)

    # Lưu kết quả
    filename = os.path.basename(input_path)
    output_path = os.path.join(output_folder, f"enhanced_{filename}")
    cv2.imwrite(output_path, enhanced_img)

    return output_path
