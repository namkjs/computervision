import cv2
import numpy as np


# Phân cụm K-Means để phân vùng ảnh
def kmeans_clustering(image, k=3, max_iter=100, epsilon=0.2):
    # Chuyển ảnh sang dạng 2D (reshape)
    Z = image.reshape((-1, 3))
    Z = np.float32(Z)

    # Tiêu chí dừng: (type, max_iter, epsilon)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, max_iter, epsilon)

    # Áp dụng K-Means
    _, labels, centers = cv2.kmeans(Z, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Chuyển đổi center về kiểu uint8 và gán nhãn lại cho ảnh
    centers = np.uint8(centers)
    segmented_image = centers[labels.flatten()]

    # Đưa ảnh về kích thước ban đầu
    segmented_image = segmented_image.reshape((image.shape))

    return segmented_image
