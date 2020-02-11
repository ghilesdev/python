import numpy
from scipy.interpolate import splprep, splev
import argparse
import cv2
import skimage.measure as measure
import numpy as np
from matplotlib import pyplot as plt

# parse arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
orig = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray_blurred = cv2.bilateralFilter(gray.copy(), 9, 75, 75)
gray_blurred_g = cv2.GaussianBlur(gray.copy(), (5, 5), 0)
# cv2.imshow('blur', gray_blurred)
# cv2.waitKey(0)

# rescaling the image for better precision
scale = 2
h, w = gray.shape
newX = w * scale
newY = h * scale
gray = cv2.resize(gray, (int(newX), int(newY)))
image = cv2.resize(image, (int(newX), int(newY)))

edges = cv2.Canny(gray, 60, 255)
edges_blurred = cv2.Canny(gray_blurred, 60, 255)
edges_blurred_g = cv2.Canny(gray_blurred_g, 60, 255)
# cv2.imshow('edges blurred', edges_blurred)
# cv2.waitKey(0)
# thresh = cv2.threshold(edges, 200, 255, cv2.THRESH_BINARY)

contours, hi = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours_b, hi_b = cv2.findContours(
    edges_blurred, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
)
contours_bg, hi_bg = cv2.findContours(
    edges_blurred_g, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
)
print(f"found {len(contours)} contours on non blurred img")
print(f"found {len(contours_b)} contours on  blurred img")
print(f"found {len(contours_bg)} contours on  blurred img")

black_image = np.zeros_like(image)
black_image_b = np.zeros_like(image)
black_image_bg = np.zeros_like(image)
cv2.drawContours(image, contours, -1, (0, 255, 0), 1)
cv2.drawContours(black_image, contours, -1, (0, 255, 0), 1)
cv2.drawContours(black_image_b, contours_b, -1, (0, 255, 0), 1)
cv2.drawContours(black_image_bg, contours_bg, -1, (0, 255, 0), 1)
# cv2.imshow('black with contours', orig)
# cv2.waitKey(0)


# finding contours with sk-Image
# contours = measure.find_contours(gray, 0.8)
# print(contours[0])
#
# # Display the image and plot all contours found
# fig, ax1 = plt.subplots()
# ax1.imshow(black_image, cmap=plt.cm.gray)
#
# # for n, contour in enumerate(contours):
# #     ax.plot(contour[:, 1], contour[:, 0], linewidth=2)
#
# ax1.axis('image')
# ax1.set_xticks([])
# ax1.set_yticks([])
# plt.show()


# #Trying to smoothen edges
# smoothened = []
# for contour in contours:
#     x,y = contour.T
#     # Convert from numpy arrays to normal arrays
#     x = x.tolist()[0]
#     y = y.tolist()[0]
#     # https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.interpolate.splprep.html
#     tck, u = splprep([x,y], u=None, s=1.0, per=1)
#     # https://docs.scipy.org/doc/numpy-1.10.1/reference/generated/numpy.linspace.html
#     u_new = numpy.linspace(u.min(), u.max(), 25)
#     # https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.interpolate.splev.html
#     x_new, y_new = splev(u_new, tck, der=0)
#     # Convert it back to numpy format for opencv to be able to display it
#     res_array = [[[int(i[0]), int(i[1])]] for i in zip(x_new,y_new)]
#     smoothened.append(numpy.asarray(res_array, dtype=numpy.int32))

# Overlay the smoothed contours on the original image
# cv2.drawContours(image, smoothened, -1, (255,0,255), 2)
# cv2.imshow('smoothened', image)
# cv2.waitKey()


plt.subplot(2, 2, 1)
plt.imshow(black_image)
plt.title("contours of upscaled image")

plt.subplot(2, 2, 2)
plt.imshow(image)
plt.title("not scaled image with contours")

plt.subplot(2, 2, 3)
plt.imshow(black_image_b)
plt.title("not scaled image with contours")

plt.subplot(2, 2, 4)
plt.imshow(black_image_bg)
plt.title("not scaled image with contours")


plt.grid(False)

# plt.tight_layout()


plt.show()

erosion_size = 0
max_elem = 2
max_kernel_size = 21
title_trackbar_element_type = "Element:\n 0: Rect \n 1: Cross \n 2: Ellipse"
title_trackbar_kernel_size = "Kernel size:\n 2n +1"
title_erosion_window = "Erosion Demo"
title_dilatation_window = "Dilation Demo"


def erosion(val):
    erosion_size = cv2.getTrackbarPos(title_trackbar_kernel_size, title_erosion_window)
    erosion_type = 0
    val_type = cv2.getTrackbarPos(title_trackbar_element_type, title_erosion_window)
    if val_type == 0:
        erosion_type = cv2.MORPH_RECT
    elif val_type == 1:
        erosion_type = cv2.MORPH_CROSS
    elif val_type == 2:
        erosion_type = cv2.MORPH_ELLIPSE
    element = cv2.getStructuringElement(
        erosion_type,
        (2 * erosion_size + 1, 2 * erosion_size + 1),
        (erosion_size, erosion_size),
    )
    erosion_dst = cv2.erode(src, element)
    cv2.imshow(title_erosion_window, erosion_dst)


def dilatation(val):
    dilatation_size = cv2.getTrackbarPos(
        title_trackbar_kernel_size, title_dilatation_window
    )
    dilatation_type = 0
    val_type = cv2.getTrackbarPos(title_trackbar_element_type, title_dilatation_window)
    if val_type == 0:
        dilatation_type = cv2.MORPH_RECT
    elif val_type == 1:
        dilatation_type = cv2.MORPH_CROSS
    elif val_type == 2:
        dilatation_type = cv2.MORPH_ELLIPSE
    element = cv2.getStructuringElement(
        dilatation_type,
        (2 * dilatation_size + 1, 2 * dilatation_size + 1),
        (dilatation_size, dilatation_size),
    )
    dilatation_dst = cv2.dilate(src, element)
    cv2.imshow(title_dilatation_window, dilatation_dst)


# parser = argparse.ArgumentParser(description='Code for Eroding and Dilating tutorial.')
# parser.add_argument('--input', help='Path to input image.', default='LinuxLogo.jpg')
# args = parser.parse_args()
# src = cv.imread(cv.samples.findFile(args.input))
src = black_image
if src is None:
    print("Could not open or find the image: ", args.input)
    exit(0)
cv2.namedWindow(title_erosion_window)
cv2.createTrackbar(
    title_trackbar_element_type, title_erosion_window, 0, max_elem, erosion
)
cv2.createTrackbar(
    title_trackbar_kernel_size, title_erosion_window, 0, max_kernel_size, erosion
)
cv2.namedWindow(title_dilatation_window)
cv2.createTrackbar(
    title_trackbar_element_type, title_dilatation_window, 0, max_elem, dilatation
)
cv2.createTrackbar(
    title_trackbar_kernel_size, title_dilatation_window, 0, max_kernel_size, dilatation
)
erosion(0)
dilatation(0)
cv2.waitKey()


# img = cv2.imread('j.png',0)
kernel = np.ones((5, 5), np.uint8)
erosion = cv2.erode(black_image, kernel, iterations=1)
# opening
opening = cv2.morphologyEx(black_image, cv2.MORPH_OPEN, kernel)
cv2.imshow("openning", opening)
cv2.waitKey(0)

# closing
closing = cv2.morphologyEx(black_image, cv2.MORPH_CLOSE, kernel)
cv2.imshow("closing", closing)
cv2.imwrite("closing.jpg", closing)
cv2.waitKey(0)
