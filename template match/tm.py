import cv2
import numpy as np
import argparse
from matplotlib import pyplot as plt

#loading argument parser
ap=argparse.ArgumentParser()
ap.add_argument("-i", "--image", help="path to image")
ap.add_argument("-t", "--template", help="path to template")
args=vars(ap.parse_args())

img_rgb = cv2.imread(args["image"])
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
template = cv2.imread(args['template'],0)
w, h = template.shape[::-1]

res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
threshold = 0.8
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

cv2.imwrite('res.png',img_rgb)
cv2.imshow('res.png',img_rgb)
cv2.waitKey(0)