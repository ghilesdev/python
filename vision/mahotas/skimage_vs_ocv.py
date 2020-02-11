import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import feature, measure
from scipy import ndimage as ndi
from skimage.color import rgb2gray
import imutils

# loading image and applying grayscale by skimage and opencv
ocv = cv2.imread("2.png")
ocv_g = cv2.cvtColor(ocv, cv2.COLOR_BGR2GRAY)
ski_g = rgb2gray(ocv)

# applying canny with skimage and opencv
canny = cv2.Canny(ocv_g, 60, 255)
canny_ski = feature.canny(ski_g, sigma=1)

# detecting contours with opencv and skimage
cnts_opencv = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts_skimage = measure.find_contours(canny_ski, 0.4)

# using function grabcontours in case drawcontours throws numpy array error
cnts_opencv = imutils.grab_contours(cnts_opencv)

# drawing contours with opencv and skimage
black = np.zeros_like(ocv)
cv2.drawContours(black, cnts_opencv, -1, (0, 255, 0), 2)

fig, axes = plt.subplots(1, 2, figsize=(8, 4))
ax = axes.ravel()
ax[0].imshow(black)
ax[0].set_title("opencv_gray")
# ax[1].imshow(canny_ski)
# ax[1].set_title('skimage_gray')

for i, c in enumerate(cnts_skimage):
    ax[1].plot(c[:, 1], c[:, 0], linewidth=2)
plt.show()
