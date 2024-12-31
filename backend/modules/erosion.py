from modules.read import *


# Erosion bằng OpenCV
def erosion_opencv(image, kernel_size=5, iterations=1):
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    eroded_image = cv2.erode(image, kernel, iterations=iterations)
    return eroded_image


# Erosion bằng thuật toán thủ công
def erosion_algorithm(image, kernel_size=3):
    pad = kernel_size // 2
    padded_image = np.pad(image, pad, mode="constant", constant_values=255)
    eroded_image = np.zeros_like(image)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            roi = padded_image[i : i + kernel_size, j : j + kernel_size]

            # Nếu tất cả pixel trong vùng kernel đều là 255 (trắng), giữ lại pixel đó
            if np.min(roi) == 255:
                eroded_image[i, j] = 255

    return eroded_image


if __name__ == "__main__":
    input_path = "static/uploads/input.png"
    output_path_algorithm_color = "static/results/erosion.png"
    output_path_opencv_color = "static/results/erosion_opencv_color.png"

    # Đọc ảnh đầu vào (màu)
    input_image_color = read_image(input_path)

    filtered_image_algorithm_color = erosion_algorithm(input_image_color["image_data"])

    filtered_image_opencv_color = erosion_opencv(input_image_color["image_data"])

    cv2.imwrite(output_path_algorithm_color, filtered_image_algorithm_color)
    cv2.imwrite(output_path_opencv_color, filtered_image_opencv_color)

    print(
        f"Ảnh màu sau khi áp dụng Mean Filter (thuật toán) đã được lưu tại: {output_path_algorithm_color}"
    )
    print(
        f"Ảnh màu sau khi áp dụng Mean Filter (OpenCV) đã được lưu tại: {output_path_opencv_color}"
    )
