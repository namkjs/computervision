from read import *


def add_salt_and_pepper_noise(image, salt_prob, pepper_prob):
    noisy_image = np.copy(image)
    row, col, ch = noisy_image.shape

    # Generate random values for each pixel
    random_matrix = np.random.rand(row, col, ch)

    # Set salt (white) pixels
    salt_coords = random_matrix < salt_prob
    noisy_image[salt_coords] = 255

    # Set pepper (black) pixels
    pepper_coords = random_matrix > (1 - pepper_prob)
    noisy_image[pepper_coords] = 0

    return noisy_image


if __name__ == "__main__":
    input_path = "static/uploads/input.png"
    output_path_algorithm_color = "static/results/salt_pepper.png"

    # Đọc ảnh đầu vào (màu)
    input_image_color = read_image(input_path)["image_data"]

    # Áp dụng bộ lọc highpass
    filtered_image_algorithm_color = add_salt_and_pepper_noise(
        input_image_color, 0.02, 0.02
    )

    cv2.imwrite(output_path_algorithm_color, filtered_image_algorithm_color)

    print(
        f"Ảnh màu sau khi áp dụng High Pass Filter đã được lưu tại: {output_path_algorithm_color}"
    )
