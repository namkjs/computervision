from flask import Flask, request, jsonify, send_file
import os
from backend.modules.enhance import enhance
from modules import preprocess, segment

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
RESULT_FOLDER = 'static/results'

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

    if not filepath or not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404

    if operation == "enhance":
        result_path = enhance.enhance_image(filepath, RESULT_FOLDER)
    elif operation == "segment":
        result_path = segment.segment_image(filepath, RESULT_FOLDER)
    else:
        return jsonify({"error": "Invalid operation"}), 400

    return jsonify({"message": "Image processed successfully", "result_path": result_path})

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    path = os.path.join(RESULT_FOLDER, filename)
    if os.path.exists(path):
        return send_file(path)
    return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
