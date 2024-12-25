from modules.read import *
import numpy as np
def power_law_transform(image, gamma, c=1):
    # Chuyển ảnh sang dạng float để tính toán
    image = np.array(image, dtype=np.float32) / 255.0
    power_image = c * np.power(image, gamma)
    power_image = np.uint8(255 * power_image)  # Chuẩn hóa về 0-255
    return power_image

input_path = "static/uploads/input.png"
input_image = read_image(input_path)
gamma = 0.1
log_image = power_law_transform(input_image['image_data'], gamma)
cv2.imwrite("static/results/power_law.png", log_image)
