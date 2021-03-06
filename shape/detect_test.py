import cv2
import argparse
import numpy as np

font = cv2.FONT_HERSHEY_COMPLEX


# loading argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help="path to image")
args = vars(ap.parse_args())

# loading image and preprocessing
img = cv2.imread(args["image"], cv2.IMREAD_GRAYSCALE)
# img = cv2.imread("shapes.jpg", cv2.IMREAD_GRAYSCALE)
threshold = cv2.threshold(img, 240, 255, cv2.THRESH_BINARY)
contours = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
    cv2.drawContours(img, [approx], 0, (0), 5)
    x = approx.ravel()[0]
    y = approx.ravel()[1]
    if len(approx) == 3:
        cv2.putText(img, "Triangle", (x, y), font, 1, (0))
    elif len(approx) == 4:
        cv2.putText(img, "Rectangle", (x, y), font, 1, (0))
    elif len(approx) == 5:
        cv2.putText(img, "Pentagon", (x, y), font, 1, (0))
    elif 6 < len(approx) < 15:
        cv2.putText(img, "Ellipse", (x, y), font, 1, (0))
    else:
        cv2.putText(img, "Circle", (x, y), font, 1, (0))

cv2.imshow("shapes", img)
cv2.imshow("Threshold", threshold)
cv2.waitKey(0)
cv2.destroyAllWindows()
