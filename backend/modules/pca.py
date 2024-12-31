import cv2
import numpy as np


# Hàm chuẩn bị dữ liệu và thực hiện PCA
def apply_pca(image, num_components=50):
    # Chuyển ảnh sang grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape

    # Reshape ảnh thành vector (flatten)
    reshaped = gray.flatten().astype(np.float32)

    # Chuẩn hóa dữ liệu (mean = 0)
    mean, eigenvectors = cv2.PCACompute(
        reshaped.reshape(1, -1), mean=None, maxComponents=num_components
    )

    # Dự đoán PCA (đưa ảnh về không gian mới)
    pca_result = np.dot(eigenvectors, reshaped - mean.flatten())

    # Khôi phục ảnh từ PCA
    restored = np.dot(pca_result, eigenvectors) + mean.flatten()
    restored_image = restored.reshape(h, w)

    return np.uint8(np.clip(restored_image, 0, 255))
