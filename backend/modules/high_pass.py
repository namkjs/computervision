from modules.read import *
import numpy as np
import cv2

def highpass_filter(image, cutoff):
    # Chuyển đổi Fourier
    dft = cv2.dft(np.float32(image), flags=cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)

    # Tạo mặt nạ thông cao
    rows, cols = image.shape
    crow, ccol = rows // 2, cols // 2
    mask = np.ones((rows, cols, 2), np.uint8)
    cv2.circle(mask, (ccol, crow), cutoff, (0, 0, 0), -1)

    # Áp dụng mặt nạ
    filtered_dft = dft_shift * mask

    # Chuyển ngược Fourier
    dft_ishift = np.fft.ifftshift(filtered_dft)
    img_back = cv2.idft(dft_ishift)
    img_back = cv2.magnitude(img_back[:, :, 0], img_back[:, :, 1])

    # Chuẩn hóa giá trị về 0-255
    img_back = np.uint8(np.clip(img_back / np.max(img_back) * 255, 0, 255))
    return img_back

def highpass_filter_color(image, cutoff):
    """
    Áp dụng bộ lọc thông cao (Highpass Filter) trên ảnh màu.
    """
    # Tách các kênh màu
    channels = cv2.split(image)
    filtered_channels = []

    for channel in channels:
        # Áp dụng highpass filter cho từng kênh
        filtered_channel = highpass_filter(channel, cutoff)
        filtered_channels.append(filtered_channel)

    # Gộp lại các kênh màu đã xử lý
    return cv2.merge(filtered_channels)

if __name__ == "__main__":
    input_path = "static/uploads/input.png"
    output_path_algorithm_color = "static/results/high_pass.png"

    # Đọc ảnh đầu vào (màu)
    input_image_color = read_image(input_path)['image_data']

    # Áp dụng bộ lọc highpass
    filtered_image_algorithm_color = highpass_filter_color(input_image_color, 10)

    # Lưu kết quả
    cv2.imwrite(output_path_algorithm_color, filtered_image_algorithm_color)

    print(f"Ảnh màu sau khi áp dụng High Pass Filter đã được lưu tại: {output_path_algorithm_color}")
