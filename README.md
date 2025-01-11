# 📸 Image Processing API

## 🔍 Giới Thiệu  
Dự án **Image Processing API** cung cấp các chức năng xử lý ảnh như tăng cường chất lượng, phục hồi và nén ảnh thông qua API được xây dựng bằng **Flask**. Dự án hỗ trợ nhiều thuật toán xử lý ảnh từ cơ bản đến nâng cao và được triển khai trên nền tảng **Render.com**.

---
## 🏗 Demo
### https://computervision-1-kcxy.onrender.com/
<img width="1117" alt="image" src="https://github.com/user-attachments/assets/487ec6c0-84ca-4dfd-967e-da0d687a5ee8" />
---

## 🚀 Tính Năng  

- **Cải thiện ảnh (Image Enhancement)**  
  - Cân bằng histogram  
  - Biến đổi logarit và power-law (gamma correction)  
  - Bộ lọc trung bình và trung vị  
  - Bộ lọc Laplacian  

- **Phục hồi ảnh (Image Restoration)**  
  - Xử lý nhiễu Gaussian, Salt-and-Pepper  
  - Bộ lọc Wiener  

- **Xử lý hình thái học (Morphological Processing)**  
  - Giãn nở (Dilation), co lại (Erosion)  
  - Mở (Opening), đóng (Closing)  

- **Phân vùng ảnh (Image Segmentation)**  
  - Ngưỡng hóa ảnh (Global, Otsu, Adaptive Thresholding)  
  - Phân cụm K-means  
  - Phân đoạn Watershed  

- **Nhận diện vật thể (Object Recognition)**  
  - Phân tích thành phần chính PCA  

- **Nén ảnh (Image Compression)**  
  - Mã hóa Huffman  
  - Nén JPEG  

---

## 🛠 Cài Đặt

### 1. Clone Repository  
```bash
git clone 
cd image-processing-api
```
### 2. Tạo môi trường ảo và cài đặt thư viện
```bash
python -m venv venv
source venv/bin/activate  # Đối với Linux/MacOS
venv\Scripts\activate     # Đối với Windows

pip install -r requirements.txt
```
### 3. Chạy Server Local
```bash
python backend/app.py
```
### 4. Truy cập Frontend
Mở file frontend/index.html trên trình duyệt để sử dụng giao diện trực quan.

