import cv2
import numpy as np
from read import *


def inverse_filter_opencv_color(image):
    # Tách các kênh màu (B, G, R)
    channels = cv2.split(image)
    result_channels = []

    # Áp dụng Inverse Filter cho từng kênh
    for channel in channels:
        dft = cv2.dft(np.float32(channel), flags=cv2.DFT_COMPLEX_OUTPUT)
        dft_shift = np.fft.fftshift(dft)

        # Chuyển đổi sang dạng biên độ và pha
        magnitude, phase = cv2.cartToPolar(dft_shift[:, :, 0], dft_shift[:, :, 1])

        # Tránh chia cho 0 (vấn đề phổ biến với inverse filter)
        magnitude = np.where(magnitude == 0, 1, magnitude)
        inverse_magnitude = 1 / magnitude

        # Chuyển ngược từ biên độ và pha về tọa độ Cart
        real, imag = cv2.polarToCart(inverse_magnitude, phase)
        dft_shift[:, :, 0] = real
        dft_shift[:, :, 1] = imag

        # Thực hiện biến đổi Fourier ngược
        dft_inverse = np.fft.ifftshift(dft_shift)
        img_back = cv2.idft(dft_inverse)
        img_back = cv2.magnitude(img_back[:, :, 0], img_back[:, :, 1])

        # Clip giá trị pixel trong khoảng [0, 255]
        result_channels.append(np.uint8(np.clip(img_back, 0, 255)))

    # Ghép lại các kênh màu đã xử lý
    return cv2.merge(result_channels)


def inverse_filter_algorithm(image):
    # Tách các kênh màu (B, G, R)
    channels = cv2.split(image)
    result_channels = []

    # Áp dụng Inverse Filter cho từng kênh
    for channel in channels:
        f = np.fft.fft2(channel)
        fshift = np.fft.fftshift(f)

        # Lấy biên độ (magnitude) của phổ Fourier
        magnitude = np.abs(fshift)

        # Tránh chia cho 0
        inverse_magnitude = np.where(magnitude == 0, 1, 1 / magnitude)

        # Áp dụng phép nghịch đảo
        fshift = fshift * inverse_magnitude

        # Biến đổi Fourier ngược
        f_ishift = np.fft.ifftshift(fshift)
        img_back = np.fft.ifft2(f_ishift)
        img_back = np.abs(img_back)

        # Clip giá trị pixel trong khoảng [0, 255]
        result_channels.append(np.uint8(np.clip(img_back, 0, 255)))

    # Ghép các kênh màu sau xử lý
    return cv2.merge(result_channels)


if __name__ == "__main__":
    input_path = "static/results/salt_pepper.png"
    output_path_algorithm_color = "static/results/inverse.png"
    output_path_opencv_color = "static/results/inverse_opencv.png"

    # Đọc ảnh đầu vào (màu)
    input_image_color = read_image(input_path)

    if input_image_color and input_image_color["image_data"] is not None:
        # Áp dụng bộ lọc inverse cho từng kênh màu
        filtered_image_algorithm_color = inverse_filter_algorithm(
            input_image_color["image_data"]
        )
        filtered_image_opencv_color = inverse_filter_opencv_color(
            input_image_color["image_data"]
        )

        # Lưu kết quả
        cv2.imwrite(output_path_algorithm_color, filtered_image_algorithm_color)
        cv2.imwrite(output_path_opencv_color, filtered_image_opencv_color)

        print(f"Ảnh màu (algorithm) lưu tại: {output_path_algorithm_color}")
        print(f"Ảnh màu (OpenCV) lưu tại: {output_path_opencv_color}")
    else:
        print("Không thể đọc ảnh đầu vào.")
