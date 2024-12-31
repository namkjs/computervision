from modules.read import *


def add_gaussian_noise(image, mean, sigma):
    row, col, ch = image.shape
    gauss = np.random.normal(mean, sigma, (row, col, ch)).astype(np.uint8)
    noisy_image = cv2.add(image, gauss)
    return noisy_image


if __name__ == "__main__":
    input_path = "static/uploads/input.png"
    output_path_algorithm_color = "static/results/gaussian.png"

    # Đọc ảnh đầu vào (màu)
    input_image_color = read_image(input_path)["image_data"]

    # Áp dụng bộ lọc highpass
    filtered_image_algorithm_color = add_gaussian_noise(input_image_color)

    cv2.imwrite(output_path_algorithm_color, filtered_image_algorithm_color)

    print(
        f"Ảnh màu sau khi áp dụng High Pass Filter đã được lưu tại: {output_path_algorithm_color}"
    )
