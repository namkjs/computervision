import cv2
import numpy as np
import heapq
from collections import defaultdict


# Tạo class Node cho cây Huffman
class HuffmanNode:
    def __init__(self, pixel_value, freq):
        self.pixel_value = pixel_value
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


# Xây dựng cây Huffman
def build_huffman_tree(hist):
    heap = [HuffmanNode(i, freq) for i, freq in enumerate(hist) if freq > 0]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0] if heap else None


# Tạo bảng mã Huffman
def generate_huffman_codes(node, code="", huffman_codes={}):
    if node is None:
        return

    if node.pixel_value is not None:
        huffman_codes[node.pixel_value] = code

    generate_huffman_codes(node.left, code + "0", huffman_codes)
    generate_huffman_codes(node.right, code + "1", huffman_codes)


# Nén ảnh bằng Huffman
def huffman_encode(image):
    # Tạo histogram của ảnh
    hist = cv2.calcHist([image], [0], None, [256], [0, 256]).flatten()

    # Xây dựng cây Huffman
    huffman_tree = build_huffman_tree(hist)

    # Tạo bảng mã Huffman
    huffman_codes = {}
    generate_huffman_codes(huffman_tree, huffman_codes=huffman_codes)

    # Mã hóa ảnh
    encoded_data = "".join([huffman_codes[pixel] for pixel in image.flatten()])

    return encoded_data, huffman_codes, image.shape


# Giải nén ảnh
def huffman_decode(encoded_data, huffman_codes, shape):
    # Đảo ngược bảng mã Huffman để giải mã
    reverse_codes = {v: k for k, v in huffman_codes.items()}

    decoded_pixels = []
    buffer = ""

    # Giải mã dữ liệu từ chuỗi nhị phân
    for bit in encoded_data:
        buffer += bit
        if buffer in reverse_codes:
            decoded_pixels.append(reverse_codes[buffer])
            buffer = ""

    # Chuyển danh sách pixel thành ảnh
    decoded_image = np.array(decoded_pixels, dtype=np.uint8).reshape(shape)

    return decoded_image
