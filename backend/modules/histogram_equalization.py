from read import *
import numpy as np  # Thêm thư viện numpy

def histogram_equalization_gray(image):

    height = len(image)
    width = len(image[0])

    # Tính histogram
    histogram = [0] * 256
    for row in image:
        for pixel in row:
            histogram[pixel] += 1

    # Tính PDF
    total_pixels = height * width
    pdf = [count / total_pixels for count in histogram]

    # Tính CDF
    cdf = [0] * 256
    cdf[0] = pdf[0]
    for i in range(1, 256):
        cdf[i] = cdf[i - 1] + pdf[i]

    # Chuyển đổi giá trị mức xám dựa trên CDF
    equalized_map = [round(c * 255) for c in cdf]

    # Tạo ảnh mới với các giá trị mức xám đã được chuyển đổi
    equalized_image = [[equalized_map[pixel] for pixel in row] for row in image]

    return equalized_image

def process_image_with_both_methods(input_path):
    input_image = read_image(input_path)
    gray_image = [[int(0.299 * pixel[0] + 0.587 * pixel[1] + 0.114 * pixel[2]) for pixel in row] for row in input_image["image_data"]]

    custom_equalized = histogram_equalization_gray(gray_image)

    custom_equalized_np = np.array(custom_equalized, dtype=np.uint8)

    gray_image_np = np.array(gray_image, dtype=np.uint8)
    opencv_equalized = cv2.equalizeHist(gray_image_np)

    return {
        "custom_equalized": custom_equalized_np,
        "opencv_equalized": opencv_equalized
    }

if __name__ == "__main__":
    input_path = "static/uploads/input.png"
    output_path_custom = "static/results/equalized_image_custom.png"
    output_path_opencv = "static/results/equalized_image_opencv.png"

    results = process_image_with_both_methods(input_path)

    # Lưu kết quả
    cv2.imwrite(output_path_custom, results["custom_equalized"])
    cv2.imwrite(output_path_opencv, results["opencv_equalized"])

    print(f"Ảnh sau khi xử lý bằng thuật toán tự triển khai đã được lưu tại: {output_path_custom}")
    print(f"Ảnh sau khi xử lý bằng OpenCV đã được lưu tại: {output_path_opencv}")