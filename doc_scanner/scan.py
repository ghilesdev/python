from mymodule.transform import four_points_transform
from skimage.filters import threshold_local, threshold_otsu, try_all_threshold
import numpy as np
import argparse
import cv2
import imutils

# loading the argument parser
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', help="path to image")
args = vars(ap.parse_args())

# loading the image, computing the ratio, cloning and resizing
image = cv2.imread(args["image"])
ratio = image.shape[0] / 500.0
orig = image.copy()
image = imutils.resize(image, height=500)

# converting to grayscale, blurring and finding edges
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(gray, 75, 200)

# showing step one
print("STEP 1: Edge Detection")
cv2.imshow('image', image)
cv2.imshow('edged', edged)
cv2.waitKey(0)
cv2.destroyAllWindows()

# finding contours and keeping largests ones
cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

# loop over the contours
for c in cnts:
    # approx the contours
    perri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * perri, True)

    # if approximated contour has four points assume we found the sceen
    if len(approx) == 4:
        screenCnt = approx
        break

# show the outline of the paper
print('STEP 2: FINDING the contours')
cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
cv2.imshow('outline', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# apply the four point transform to obtain a top-down
# view of the original image
warped = four_points_transform(orig, screenCnt.reshape(4, 2) * ratio)

# convert to grayscale then thresholding finaly apply black and white effect
warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
#thres=threshold_otsu(warped)
T = threshold_local(warped, 11,  offset=10, method='gaussian')
warped = (warped > T).astype('uint8') * 255

# step 3
print('STEP 3: apply perspective transformation')
cv2.imshow('original', imutils.resize(orig, height=650))
cv2.imshow('scanned', imutils.resize(warped, height=650))
cv2.waitKey(0)
cv2.destroyAllWindows()


