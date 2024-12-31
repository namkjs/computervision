from modules.read import *


# Opening bằng OpenCV (Erosion + Dilation)
def opening_opencv(image, kernel_size=5, iterations=1):
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    opened_image = cv2.morphologyEx(
        image, cv2.MORPH_OPEN, kernel, iterations=iterations
    )
    return opened_image


# Closing bằng OpenCV (Dilation + Erosion)
def closing_opencv(image, kernel_size=5, iterations=1):
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    closed_image = cv2.morphologyEx(
        image, cv2.MORPH_CLOSE, kernel, iterations=iterations
    )
    return closed_image


# Opening thủ công (Erosion + Dilation)
def opening_algorithm(image, kernel_size=3):
    eroded = erosion_algorithm(image, kernel_size)
    opened_image = dilation_algorithm(eroded, kernel_size)
    return opened_image


# Closing thủ công (Dilation + Erosion)
def closing_algorithm(image, kernel_size=3):
    dilated = dilation_algorithm(image, kernel_size)
    closed_image = erosion_algorithm(dilated, kernel_size)
    return closed_image


# Hàm erosion và dilation thủ công
def erosion_algorithm(image, kernel_size=3):
    pad = kernel_size // 2
    padded_image = np.pad(image, pad, mode="constant", constant_values=255)
    eroded_image = np.zeros_like(image)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            roi = padded_image[i : i + kernel_size, j : j + kernel_size]
            if np.min(roi) == 255:
                eroded_image[i, j] = 255
    return eroded_image


def dilation_algorithm(image, kernel_size=3):
    pad = kernel_size // 2
    padded_image = np.pad(image, pad, mode="constant", constant_values=0)
    dilated_image = np.zeros_like(image)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            roi = padded_image[i : i + kernel_size, j : j + kernel_size]
            dilated_image[i, j] = np.max(roi)
    return dilated_image
