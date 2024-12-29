from flask import Flask, request, jsonify, send_file
import os
import cv2
import numpy as np
from flask_cors import CORS

from modules.laplacian import laplacian_filter_algorithm_color, laplacian_filter_opencv_color
from modules.high_pass import highpass_filter_color
from modules.low_pass import lowpass_filter_color
from modules.histogram_equalization import *
from modules.logarithmic import *
from modules.preprocess import *
from modules.mean_filter import *
from modules.median_filter import *
from modules.power_law import * 
app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
RESULT_FOLDER = 'static/results'
CORS(app, resources={r"/upload": {"origins": "http://127.0.0.1:8000"}})
CORS(app, resources={r"/process": {"origins": "http://127.0.0.1:8000"}})

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return "Image Processing API is running!"

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    return jsonify({"message": "File uploaded successfully", "filepath": filepath})

@app.route('/process', methods=['POST'])
def process_image():
    data = request.get_json()
    filepath = data.get('filepath')
    operation = data.get('operation')
    params = data.get('params', {})

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
        result_image = median_filter_algorithm_color(input_image, kernel_size=kernel_size)
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
    else:
        return jsonify({"error": "Invalid operation"}), 400

    temp_result_path = os.path.join(RESULT_FOLDER, "temp_result.jpg")
    cv2.imwrite(temp_result_path, result_image)

    return send_file(temp_result_path, mimetype='image/jpeg')



@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    path = os.path.join(RESULT_FOLDER, filename)
    if os.path.exists(path):
        return send_file(path)
    return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
