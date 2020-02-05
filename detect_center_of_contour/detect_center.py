import argparse
import imutils
import cv2
from matplotlib import pyplot as plt
import copy
import numpy as np


#loading argument parser
ap=argparse.ArgumentParser()
ap.add_argument("-i", "--image", help="path to image")
args=vars(ap.parse_args())

#loading image and preprocessing
img=cv2.imread(args["image"])
orig=img.copy()
#imgCopy =  copy.deepcopy(img)
gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred=cv2.GaussianBlur(gray, (5,5), 0)
cv2.imshow("blurred", blurred)
cv2.imshow("orig", orig)
thresh=cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
cv2.imshow('thresh', thresh)

#finding contours
cnts=cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                      cv2.CHAIN_APPROX_SIMPLE)
cnts=imutils.grab_contours(cnts)
print(len(cnts))

font = cv2.FONT_HERSHEY_COMPLEX


#loop over the contours
for c in cnts:
    approx = cv2.approxPolyDP(c, 0.04 * cv2.arcLength(c, True), True)
    cv2.drawContours(img, [approx], 0, (0), 5)
    x = approx.ravel()[0]
    y = approx.ravel()[1]
    if len(approx) == 3:
        cv2.putText(img, "Triangle", (x, y), font, 0.5, (0,255,0))
        print(f'triangle at coords{(x,y)}')
    elif len(approx) == 4:
        cv2.putText(img, "Rectangle", (x, y), font, 0.5, (0,255,0))
        print(f'rectangle at coords{(x,y)}')
    elif len(approx) == 5:
        cv2.putText(img, "Pentagon", (x, y), font, 0.5, (0,255,0))
        print(f'pentagon at coords{(x,y)}')
    elif 6 < len(approx) < 15:
        cv2.putText(img, "Ellipse", (x, y), font, 0.5, (0,255,0))
        print(f'elipse at coords{(x,y)}')
    else:
        cv2.putText(img, "Circle", (x, y), font, 0.5, (0,255,0))
    #print(type(c))
    #print(c.shape)
    #print(len(c))



    #capture the center of the contour
    M=cv2.moments(c)
    #add 1e-10 to avoid devision by zero
    cx=int(M["m10"]/(M["m00"]+1e-10))
    cy=int(M["m01"]/(M["m00"]+1e-10))


    #drawing the contour and its center
    # cv2.drawContours(img, [c], -1, (0,255,0), 2)
    # cv2.circle(img, (cx, cy), 3, (255, 255, 255), -1)
    #cv2.putText(img, "center {};{}".format(cx, cy), (cx-20, cy-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)
cv2.imshow("img", img)
cv2.waitKey(0)




