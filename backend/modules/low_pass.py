from modules.read import *

def lowpass_filter(image, cutoff):
    # Chuyển đổi Fourier
    dft = cv2.dft(np.float32(image), flags=cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)

    rows, cols = image.shape
    crow, ccol = rows // 2, cols // 2
    mask = np.zeros((rows, cols, 2), np.uint8)
    cv2.circle(mask, (ccol, crow), cutoff, (1, 1, 1), -1)

    filtered_dft = dft_shift * mask

    dft_ishift = np.fft.ifftshift(filtered_dft)
    img_back = cv2.idft(dft_ishift)
    img_back = cv2.magnitude(img_back[:, :, 0], img_back[:, :, 1])

    return np.uint8(img_back / np.max(img_back) * 255)
def lowpass_filter_color(image, cutoff):

    channels = cv2.split(image)
    filtered_channels = []

    for channel in channels:
        filtered_channel = lowpass_filter(channel, cutoff)
        filtered_channels.append(filtered_channel)

    # Gộp lại các kênh màu đã xử lý
    return cv2.merge(filtered_channels)

if __name__ == "__main__":
    input_path = "static/uploads/input.png"
    output_path_algorithm_color = "static/results/low_pass.png"

    # Đọc ảnh đầu vào (màu)
    input_image_color = read_image(input_path)

    filtered_image_algorithm_color = lowpass_filter_color(input_image_color['image_data'], 30)


    cv2.imwrite(output_path_algorithm_color, filtered_image_algorithm_color)

    print(f"Ảnh màu sau khi áp dụng Low pass Filter (thuật toán) đã được lưu tại: {output_path_algorithm_color}")
