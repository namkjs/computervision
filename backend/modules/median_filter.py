from modules.read import *
def median_filter_algorithm(image, kernel_size=3):
    height, width = image.shape
    pad = kernel_size // 2
    padded_image = np.pad(image, pad, mode='constant', constant_values=0)
    filtered_image = np.zeros_like(image, dtype=np.float32)

    for i in range(height):
        for j in range(width):
            region = padded_image[i:i + kernel_size, j:j + kernel_size]
            filtered_image[i, j] = np.median(region)

    return np.uint8(filtered_image)

def median_filter_opencv(image, kernel_size=3):

    return cv2.medianBlur(image, kernel_size)

def median_filter_algorithm_color(image, kernel_size=3):

    channels = cv2.split(image)
    filtered_channels = []

    for channel in channels:
        filtered_channel = median_filter_algorithm(channel, kernel_size)
        filtered_channels.append(filtered_channel)

    return cv2.merge(filtered_channels)

if __name__ == "__main__":
    input_path = "static/uploads/input.png"
    output_path_algorithm_color = "static/results/median_filter_algorithm_color.png"
    output_path_opencv_color = "static/results/median_filter_opencv_color.png"

    input_image_color = read_image(input_path)

    filtered_image_algorithm_color = median_filter_algorithm_color(input_image_color['image_data'], kernel_size=3)

    filtered_image_opencv_color = median_filter_opencv(input_image_color["image_data"], kernel_size=3)

    cv2.imwrite(output_path_algorithm_color, filtered_image_algorithm_color)
    cv2.imwrite(output_path_opencv_color, filtered_image_opencv_color)

    print(f"Ảnh màu sau khi áp dụng median Filter (thuật toán) đã được lưu tại: {output_path_algorithm_color}")
    print(f"Ảnh màu sau khi áp dụng median Filter (OpenCV) đã được lưu tại: {output_path_opencv_color}")
