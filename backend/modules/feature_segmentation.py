import cv2
import numpy as np


# Phân vùng ảnh bằng Watershed Segmentation
def watershed_segmentation(image):
    # Chuyển sang ảnh xám
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Làm mờ ảnh để giảm nhiễu
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Tạo ảnh nhị phân bằng ngưỡng hóa Otsu
    _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Áp dụng phép toán Morphology để loại bỏ nhiễu nhỏ
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=2)

    # Tìm vùng nền (background) bằng phép Dilation
    sure_bg = cv2.dilate(opening, kernel, iterations=3)

    # Tìm vùng tiền cảnh (foreground) bằng khoảng cách Euclidean
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist_transform, 0.5 * dist_transform.max(), 255, 0)

    # Xác định vùng không chắc chắn (unknown) giữa nền và tiền cảnh
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)

    # Gán nhãn cho vùng tiền cảnh
    _, markers = cv2.connectedComponents(sure_fg)

    # Đánh dấu vùng chưa xác định là 0
    markers = markers + 1
    markers[unknown == 255] = 0

    # Áp dụng Watershed
    cv2.watershed(image, markers)
    image[markers == -1] = [0, 0, 255]  # Vẽ biên bằng màu đỏ

    return image
