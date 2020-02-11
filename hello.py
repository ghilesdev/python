import numpy as np
import argparse
import imutils
import cv2


# load the argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-i", ("--image"), help="path to image")
args = vars(ap.parse_args())


# load image
img = cv2.imread(args["image"])

# finding black shapes
lower = [0, 0, 0]
upper = [15, 15, 15]
shape_mask = cv2.inRange(img, lower, upper)
cv2.imshow("mask", shape_mask)
