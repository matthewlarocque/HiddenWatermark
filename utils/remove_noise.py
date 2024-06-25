import cv2
import numpy as np

def denoise_image(filename):
    # 读取图像
    img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    
    # 使用中值滤波器去除噪点
    denoised = cv2.medianBlur(img, 5)
    
    # 使用二值化操作强调主要元素
    _, thresholded = cv2.threshold(denoised, 127, 255, cv2.THRESH_BINARY)

    # 使用形态学操作进一步去除噪点并强调主要元素
    kernel = np.ones((3,3), np.uint8)
    opened = cv2.morphologyEx(thresholded, cv2.MORPH_OPEN, kernel)
    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)

    return closed

# 使用函数处理图像并保存结果
result = denoise_image("d.png")
cv2.imwrite("denoised.png", result)
