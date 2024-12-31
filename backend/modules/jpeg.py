import cv2
import os


# Nén ảnh theo tiêu chuẩn JPEG
def compress_to_jpeg(image, quality=90):
    # Tạo file tạm thời để lưu ảnh JPEG
    temp_path = "static/results/compressed.jpg"

    # Nén ảnh với mức chất lượng (quality) từ 0 đến 100
    cv2.imwrite(temp_path, image, [cv2.IMWRITE_JPEG_QUALITY, quality])

    return temp_path
