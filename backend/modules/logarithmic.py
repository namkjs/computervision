import numpy as np
from modules.read import *

def log_transform(image, c):
    image = np.array(image, dtype=np.float32)
    log_image = c * np.log(1 + image)
    log_image = np.uint8(255 * log_image / np.max(log_image)) 
    return log_image

# input_path = "static/uploads/input.png"
# input_image = read_image(input_path)
# log_image = log_transform(input_image['image_data'])
# cv2.imwrite("static/results/log_image.png", log_image)
