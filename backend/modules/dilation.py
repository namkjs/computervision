from modules.read import *


def dilation_opencv(image, kernel_size=5, iterations=1):
    # Tạo kernel (nhân) cho phép Dilation
    kernel = np.ones((kernel_size, kernel_size), np.uint8)

    # Áp dụng phép Dilation
    dilated_image = cv2.dilate(image, kernel, iterations=iterations)

    return dilated_image


def dilation_algorithm(image, kernel_size=5):
    # Kích thước kernel (vuông)
    pad = kernel_size // 2
    padded_image = np.pad(image, pad, mode="constant", constant_values=0)

    dilated_image = np.zeros_like(image)

    # Quét từng pixel và áp dụng Dilation
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            # Trích xuất vùng ảnh con (roi)
            roi = padded_image[i : i + kernel_size, j : j + kernel_size]

            # Thay vì set 255 toàn bộ, ta lấy max của vùng kernel (giống OpenCV)
            dilated_image[i, j] = np.max(roi)

    return dilated_image


if __name__ == "__main__":
    input_path = "static/uploads/input.png"
    output_path_algorithm_color = "static/results/dilation.png"
    output_path_opencv_color = "static/results/dilation_opencv.png"

    # Đọc ảnh đầu vào (màu)
    input_image_color = read_image(input_path)

    filtered_image_algorithm_color = dilation_algorithm(input_image_color["image_data"])

    filtered_image_opencv_color = dilation_opencv(input_image_color["image_data"])

    cv2.imwrite(output_path_algorithm_color, filtered_image_algorithm_color)
    cv2.imwrite(output_path_opencv_color, filtered_image_opencv_color)

    print(
        f"Ảnh màu sau khi áp dụng dilation (thuật toán) đã được lưu tại: {output_path_algorithm_color}"
    )
    print(
        f"Ảnh màu sau khi áp dụng dilation (OpenCV) đã được lưu tại: {output_path_opencv_color}"
    )
