import cv2
import numpy as np
from modules.read import *


def wiener_filter_channel(channel, kernel_size, noise_var=0.01):
    # Biến đổi Fourier của ảnh đầu vào
    f = np.fft.fft2(channel)
    fshift = np.fft.fftshift(f)

    # Tạo kernel Gaussian trong miền tần số
    rows, cols = channel.shape
    crow, ccol = rows // 2, cols // 2
    kernel = np.zeros((rows, cols))
    r = kernel_size // 2
    cv2.circle(kernel, (ccol, crow), r, 1, -1)

    # Biến đổi Fourier của kernel
    kernel_fft = np.fft.fft2(kernel)
    kernel_fft = np.fft.fftshift(kernel_fft)

    # Áp dụng Wiener Filter
    H_conj = np.conj(kernel_fft)
    H_abs2 = np.abs(kernel_fft) ** 2
    Wiener_filter = H_conj / (H_abs2 + noise_var)

    # Khôi phục ảnh bằng Wiener Filter
    result_shift = fshift * Wiener_filter
    result_ishift = np.fft.ifftshift(result_shift)
    img_back = np.fft.ifft2(result_ishift)
    img_back = np.abs(img_back)

    return np.uint8(np.clip(img_back, 0, 255))


def wiener_filter_color(image, kernel_size=30, noise_var=0.01):
    # Tách kênh màu (B, G, R)
    channels = cv2.split(image)
    result_channels = []

    # Áp dụng Wiener Filter cho từng kênh màu
    for channel in channels:
        filtered_channel = wiener_filter_channel(channel, kernel_size, noise_var)
        result_channels.append(filtered_channel)

    # Ghép kênh màu sau khi xử lý
    return cv2.merge(result_channels)


if __name__ == "__main__":
    input_path = "static/uploads/input.png"
    output_path_wiener = "static/results/wiener_filtered.png"

    # Đọc ảnh đầu vào
    input_image_color = read_image(input_path)

    if input_image_color and input_image_color["image_data"] is not None:
        # Áp dụng Wiener Filter cho ảnh màu
        filtered_image_color = wiener_filter_color(
            input_image_color["image_data"], kernel_size=30, noise_var=0.01
        )

        # Lưu ảnh kết quả
        cv2.imwrite(output_path_wiener, filtered_image_color)

        print(
            f"Ảnh màu sau khi áp dụng Wiener Filter được lưu tại: {output_path_wiener}"
        )
    else:
        print("Không thể đọc ảnh đầu vào.")
