import cv2
import PIL.Image as Image
import numpy as np
import imutils
import matplotlib.pyplot as plt

# load the image
image = cv2.imread("4.png")
# upscale
scale_factor = 3
w, h = image.shape[1], image.shape[0]
new_w, new_h = w * scale_factor, h * scale_factor
upscaled = cv2.resize(image, (new_w, new_h))
# grayscale
gray = cv2.cvtColor(upscaled, cv2.COLOR_BGR2GRAY)
# blur
blur = cv2.GaussianBlur(gray, (5, 5), 3)
# canny
canny = cv2.Canny(blur, 50, 150)
# contours
cnts = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
black = np.zeros_like(upscaled)
black_b = np.zeros_like(upscaled)
# draw approximated contours
for c in cnts:
    approx = cv2.approxPolyDP(c, 0.01 * cv2.arcLength(c, True), True)
    cv2.drawContours(upscaled, [approx], -1, (0, 255, 0), 2)


# draw contours
cv2.drawContours(black_b, cnts, -1, (0, 255, 0), 2)

# downscale
downscaled = cv2.resize(black, (w, h))

plt.subplot(1, 2, 1)
plt.imshow(upscaled)
plt.title("approximated contours")
plt.subplot(1, 2, 2)
plt.imshow(black_b)
plt.title("contours")
plt.show()
