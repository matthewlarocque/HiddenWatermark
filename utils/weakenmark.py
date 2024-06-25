import cv2
import numpy as np

img = cv2.imread('bz.png') 

# Canny边缘检测
edges = cv2.Canny(img, 100, 200) 

# 椒盐噪声
noise_num = int(img.size * 0.0003) #减小噪声比例
for i in range(noise_num):
    x = np.random.randint(0, img.shape[0]-1) 
    y = np.random.randint(0, img.shape[1]-1)
    # 仅在边缘附近区域添加噪声
    if edges[x,y] > 0 or edges[x,y+1] > 0 or edges[x+1,y] > 0:  
        if np.random.randint(0,1) == 0:
            img[x,y] = 0
        else:
            img[x,y] = 255
img = cv2.imencode('.png', img)[1]
img = cv2.imdecode(img, 1)

img = cv2.GaussianBlur(img, (3,3), 0)

cv2.imwrite('coche.png', img)