from modules.read import *

def mean_filter_algorithm(image, kernel_size=3):
    height, width = image.shape
    pad = kernel_size // 2
    padded_image = np.pad(image, pad, mode='constant', constant_values=0)
    filtered_image = np.zeros_like(image, dtype=np.float32)

    for i in range(height):
        for j in range(width):
            # Lấy vùng lân cận (kernel)
            region = padded_image[i:i + kernel_size, j:j + kernel_size]
            # Tính trung bình và gán giá trị
            filtered_image[i, j] = np.mean(region)

    return np.uint8(filtered_image)
def mean_filter_algorithm_color(image, kernel_size):

    # Tách ảnh thành các kênh màu
    channels = cv2.split(image)
    filtered_channels = []

    for channel in channels:
        filtered_channel = mean_filter_algorithm(channel, kernel_size)
        filtered_channels.append(filtered_channel)

    # Gộp các kênh màu sau khi xử lý
    return cv2.merge(filtered_channels)


def mean_filter_opencv_color(image, kernel_size):
    return cv2.blur(image, (kernel_size, kernel_size))


if __name__ == "__main__":
    input_path = "static/uploads/input.png"
    output_path_algorithm_color = "static/results/mean_filter_algorithm_color.png"
    output_path_opencv_color = "static/results/mean_filter_opencv_color.png"

    # Đọc ảnh đầu vào (màu)
    input_image_color = read_image(input_path)

    filtered_image_algorithm_color = mean_filter_algorithm_color(input_image_color['image_data'], kernel_size=3)

    filtered_image_opencv_color = mean_filter_opencv_color(input_image_color["image_data"], kernel_size=3)

    cv2.imwrite(output_path_algorithm_color, filtered_image_algorithm_color)
    cv2.imwrite(output_path_opencv_color, filtered_image_opencv_color)

    print(f"Ảnh màu sau khi áp dụng Mean Filter (thuật toán) đã được lưu tại: {output_path_algorithm_color}")
    print(f"Ảnh màu sau khi áp dụng Mean Filter (OpenCV) đã được lưu tại: {output_path_opencv_color}")
