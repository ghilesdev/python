import cv2
import numpy as np
from matplotlib import pyplot as plt
from autocanny import auto_canny


# loading image
# img0 = cv2.imread('SanFrancisco.jpg',)
img0 = cv2.imread("2.png",)

# converting to gray scale
gray = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)

# remove noise
img = cv2.GaussianBlur(gray, (3, 3), 0)

# convolute with proper kernels
laplacian = cv2.Laplacian(img, cv2.CV_64F)
sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)  # x
sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=5)  # y

# canny
canny = cv2.Canny(img, 60, 200)
cv2.imshow("canny", canny)
cv2.waitKey(0)
autoCanny = auto_canny(img)
cv2.imshow("auto canny", autoCanny)
cv2.waitKey(0)

# finding contours
cnts, h = cv2.findContours(sobelx, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img0, cnts, -1, (0, 255, 0), 2)
cv2.imshow("edges over laplacian", img0)
cv2.waitKey(0)

plt.subplot(2, 2, 1), plt.imshow(img, cmap="gray")
plt.title("Original"), plt.xticks([]), plt.yticks([])
plt.subplot(2, 2, 2), plt.imshow(laplacian, cmap="gray")
plt.title("Laplacian"), plt.xticks([]), plt.yticks([])
plt.subplot(2, 2, 3), plt.imshow(sobelx, cmap="gray")
plt.title("Sobel X"), plt.xticks([]), plt.yticks([])
plt.subplot(2, 2, 4), plt.imshow(sobely, cmap="gray")
plt.title("Sobel Y"), plt.xticks([]), plt.yticks([])

plt.show()
