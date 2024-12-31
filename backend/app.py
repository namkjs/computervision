from flask import Flask, request, jsonify, send_file
import os
import cv2
import numpy as np
from flask_cors import CORS

from modules.laplacian import (
    laplacian_filter_algorithm_color,
    laplacian_filter_opencv_color,
)
from modules.high_pass import highpass_filter_color
from modules.low_pass import lowpass_filter_color
from modules.histogram_equalization import *
from modules.logarithmic import *
from modules.preprocess import *
from modules.mean_filter import *
from modules.median_filter import *
from modules.power_law import *
from modules.gaussian import *
from modules.dilation import *
from modules.wiener_filterring import *
from modules.erosion import *
from modules.morphology import (
    opening_opencv,
    closing_opencv,
    opening_algorithm,
    closing_algorithm,
)
from modules.threshold import global_threshold, otsu_threshold, adaptive_threshold
from modules.clustering import kmeans_clustering
from modules.feature_segmentation import watershed_segmentation
from modules.pca import apply_pca
from modules.color_transform import rgb_to_ycbcr, ycbcr_to_rgb, rgb_to_hsv, hsv_to_rgb
from modules.huffman import huffman_encode, huffman_decode
from modules.jpeg import compress_to_jpeg

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
RESULT_FOLDER = "static/results"
CORS(app)

CORS(app, resources={r"/upload": {"origins": "http://localhost:8000/"}})
CORS(app, resources={r"/process": {"origins": "http://localhost:8000/"}})

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)
encoded_storage = {}


@app.route("/")
def home():
    return "Image Processing API is running!"


@app.route("/upload", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    return jsonify({"message": "File uploaded successfully", "filepath": filepath})


@app.route("/process", methods=["POST"])
def process_image():
    data = request.get_json()
    filepath = data.get("filepath")
    operation = data.get("operation")
    params = data.get("params", {})

    if not filepath or not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404

    input_image = cv2.imread(filepath)

    if input_image is None:
        return jsonify({"error": "Invalid image file"}), 400

    result_image = None

    if operation == "laplacian_opencv":
        result_image = laplacian_filter_opencv_color(input_image)
    elif operation == "laplacian_algorithm":
        result_image = laplacian_filter_algorithm_color(input_image)
    elif operation == "highpass":
        cutoff = params.get("cutoff", 30)
        result_image = highpass_filter_color(input_image, cutoff=cutoff)
    elif operation == "lowpass":
        cutoff = params.get("cutoff", 30)
        result_image = lowpass_filter_color(input_image, cutoff=cutoff)
    elif operation == "power_law":
        gamma = params.get("gamma", 1.0)
        result_image = power_law_transform(input_image, gamma=gamma)
    elif operation == "mean_filter_algorithm":
        kernel_size = params.get("kernel_size", 3)
        result_image = mean_filter_algorithm_color(input_image, kernel_size=kernel_size)
    elif operation == "mean_filter_opencv":
        kernel_size = params.get("kernel_size", 3)
        result_image = mean_filter_opencv_color(input_image, kernel_size=kernel_size)
    elif operation == "median_filter_algorithm":
        kernel_size = params.get("kernel_size", 3)
        result_image = median_filter_algorithm_color(
            input_image, kernel_size=kernel_size
        )
    elif operation == "gray":
        result_image = gray(input_image)
    elif operation == "histogram_opencv":
        result_image = histogram_opencv(input_image)
    elif operation == "histogram":
        result_image = histogram_equalization_gray(input_image)
    elif operation == "logarithmic":
        c = params.get("c", 1)
        result_image = log_transform(input_image, c)
    elif operation == "powerlaw":
        gamma = params.get("gamma", 0.1)
        c = params.get("c", 1)
        result_image = power_law_transform(input_image, gamma, c)
    elif operation == "gaussian_noise":
        mean = params.get("mean", 0)
        sigma = params.get("sigma", 25)
        result_image = add_gaussian_noise(input_image, mean=mean, sigma=sigma)
    elif operation == "salt_pepper":
        salt_prob = params.get("salt", 0.02)
        pepper_prob = params.get("pepper", 0.02)
        result_image = add_gaussian_noise(input_image, salt_prob, pepper_prob)
    elif operation == "dilation_opencv":
        kernel_size = params.get("kernel_size", 5)
        iterations = params.get("iterations", 1)
        result_image = dilation_opencv(input_image, kernel_size, iterations)
    elif operation == "dilation_algorithm":
        kernel_size = params.get("kernel_size", 3)
        result_image = dilation_algorithm(input_image, kernel_size)
    elif operation == "wiener_filter":
        kernel_size = params.get("kernel_size", 30)
        noise_var = params.get("noise_var", 0.01)
        result_image = wiener_filter_color(input_image, kernel_size, noise_var)
    elif operation == "erosion_opencv":
        kernel_size = params.get("kernel_size", 5)
        iterations = params.get("iterations", 1)
        result_image = erosion_opencv(input_image, kernel_size, iterations)
    elif operation == "opening_opencv":
        kernel_size = params.get("kernel_size", 5)
        iterations = params.get("iterations", 1)
        result_image = opening_opencv(input_image, kernel_size, iterations)

    # Thêm phép Closing bằng OpenCV
    elif operation == "closing_opencv":
        kernel_size = params.get("kernel_size", 5)
        iterations = params.get("iterations", 1)
        result_image = closing_opencv(input_image, kernel_size, iterations)

    # Thêm phép Opening bằng thuật toán thủ công
    elif operation == "opening_algorithm":
        kernel_size = params.get("kernel_size", 3)
        result_image = opening_algorithm(input_image, kernel_size)

    # Thêm phép Closing bằng thuật toán thủ công
    elif operation == "closing_algorithm":
        kernel_size = params.get("kernel_size", 3)
        result_image = closing_algorithm(input_image, kernel_size)
    # Thêm phép Erosion bằng thuật toán thủ công
    elif operation == "erosion_algorithm":
        kernel_size = params.get("kernel_size", 3)
        result_image = erosion_algorithm(input_image, kernel_size)
    elif operation == "global_threshold":
        threshold = params.get("threshold", 127)
        result_image = global_threshold(input_image, threshold)

    # Ngưỡng hóa Otsu
    elif operation == "otsu_threshold":
        result_image = otsu_threshold(input_image)

    # Ngưỡng hóa thích nghi
    elif operation == "adaptive_threshold":
        block_size = params.get("block_size", 11)
        C = params.get("C", 2)
        result_image = adaptive_threshold(input_image, block_size, C)
    elif operation == "kmeans_clustering":
        k = params.get("k", 3)
        max_iter = params.get("max_iter", 100)
        epsilon = params.get("epsilon", 0.2)
        result_image = kmeans_clustering(input_image, k, max_iter, epsilon)
    elif operation == "watershed":
        result_image = watershed_segmentation(input_image)
    elif operation == "pca":
        num_components = params.get("num_components", 50)
        result_image = apply_pca(input_image, num_components)
    elif operation == "rgb_to_ycbcr":
        result_image = rgb_to_ycbcr(input_image)
    elif operation == "ycbcr_to_rgb":
        result_image = ycbcr_to_rgb(input_image)
    elif operation == "rgb_to_hsv":
        result_image = rgb_to_hsv(input_image)
    elif operation == "hsv_to_rgb":
        result_image = hsv_to_rgb(input_image)
    elif operation == "huffman_encode":
        encoded_data, huffman_codes, shape = huffman_encode(input_image)
        encoded_storage[filepath] = (encoded_data, huffman_codes, shape)
        return jsonify(
            {
                "message": "Image compressed successfully",
                "encoded_length": len(encoded_data),
            }
        )

    # Giải nén ảnh bằng Huffman
    elif operation == "huffman_decode":
        if filepath not in encoded_storage:
            return jsonify({"error": "No encoded data found for this image"}), 404

        encoded_data, huffman_codes, shape = encoded_storage[filepath]
        result_image = huffman_decode(encoded_data, huffman_codes, shape)
    elif operation == "jpeg_compress":
        quality = params.get("quality", 90)
        result_path = compress_to_jpeg(input_image, quality)
        return send_file(
            result_path,
            mimetype="image/jpeg",
            as_attachment=True,
            download_name="compressed.jpg",
        )

    else:
        return jsonify({"error": "Invalid operation"}), 400

    temp_result_path = os.path.join(RESULT_FOLDER, "temp_result.jpg")
    cv2.imwrite(temp_result_path, result_image)

    return send_file(temp_result_path, mimetype="image/jpeg")


@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    path = os.path.join(RESULT_FOLDER, filename)
    if os.path.exists(path):
        return send_file(path)
    return jsonify({"error": "File not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
