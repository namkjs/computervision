from modules.read import *
def laplacian_filter_opencv_color(image):

    # Tách các kênh màu
    channels = cv2.split(image)
    filtered_channels = []

    for channel in channels:
        filtered_channel = cv2.Laplacian(channel, cv2.CV_64F)
        filtered_channels.append(np.uint8(np.clip(filtered_channel, 0, 255)))

    # Gộp lại các kênh màu đã xử lý
    return cv2.merge(filtered_channels)

def laplacian_filter_algorithm(image):
    kernel = np.array([[0, 1, 0],
                       [1, -4, 1],
                       [0, 1, 0]])
    height, width = image.shape
    pad = 1  # Kích thước kernel 3x3 -> pad = 1
    padded_image = np.pad(image, pad, mode='constant', constant_values=0)
    filtered_image = np.zeros_like(image, dtype=np.float32)

    for i in range(height):
        for j in range(width):
            region = padded_image[i:i + 3, j:j + 3]
            filtered_image[i, j] = np.sum(region * kernel)

    return np.uint8(np.clip(filtered_image, 0, 255))
def laplacian_filter_algorithm_color(image):

    # Tách các kênh màu
    channels = cv2.split(image)
    filtered_channels = []

    for channel in channels:
        filtered_channel = laplacian_filter_algorithm(channel)
        filtered_channels.append(filtered_channel)

    # Gộp lại các kênh màu đã xử lý
    return cv2.merge(filtered_channels)
if __name__ == "__main__":
    input_path = "static/uploads/input.png"
    output_path_algorithm_color = "static/results/laplacian.png"
    output_path_opencv_color = "static/results/laplacian_opencv.png"

    # Đọc ảnh đầu vào (màu)
    input_image_color = read_image(input_path)

    filtered_image_algorithm_color = laplacian_filter_algorithm_color(input_image_color['image_data'])

    filtered_image_opencv_color = laplacian_filter_opencv_color(input_image_color["image_data"])

    cv2.imwrite(output_path_algorithm_color, filtered_image_algorithm_color)
    cv2.imwrite(output_path_opencv_color, filtered_image_opencv_color)

    print(f"Ảnh màu sau khi áp dụng Laplacian Filter (thuật toán) đã được lưu tại: {output_path_algorithm_color}")
    print(f"Ảnh màu sau khi áp dụng Laplacian Filter (OpenCV) đã được lưu tại: {output_path_opencv_color}")
