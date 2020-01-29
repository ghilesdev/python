import argparse
import imutils
import cv2
import numpy as np


#loading argument parser
ap=argparse.ArgumentParser()
ap.add_argument("-i", "--image", help="path to image")
args=vars(ap.parse_args())

#loading image and preprocessing
img=cv2.imread(args["image"])
gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred=cv2.GaussianBlur(gray, (5,5), 0)
thresh=cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

#finding contours
cnts=cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, 
                      cv2.CHAIN_APPROX_SIMPLE)
cnts=imutils.grab_contours(cnts)

#loop over the contours
for c in cnts:
    #print(type(c))
    #print(c.shape)
    #print(c)
    
    
    #capture the center of the contour
    M=cv2.moments(c)
    cx=int(M["m10"]/(M["m00"]+1e-10))
    cy=int(M["m01"]/(M["m00"]+1e-10))
    
    #drawing the contour and its center
    cv2.drawContours(img, [c], -1, (0,255,0), 2)
    cv2.circle(img, (cx, cy), 3, (255, 255, 255), -1)
    cv2.putText(img, "center {};{}".format(cx, cy), (cx-20, cy-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 
                (255, 0, 255), 1)
    
 
cv2.imshow("img", img)
cv2.waitKey(0)


