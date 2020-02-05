import numpy as np 
import argparse
import imutils
import cv2


#load the argument parser 
ap=argparse.ArgumentParser()
ap.add_argument('-i', ('--image'), help='path to image')
args=vars(ap.parse_args())


#load image
img= cv2.imread(args['image'])

#finding black shapes 
lower=np.array([0,0,0])
upper=np.array([30,30,30])
shape_mask=cv2.inRange(img, lower, upper)

#finding countours
cnts=cv2.findContours(shape_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts=imutils.grab_contours(cnts)
print("found {} contours".format(len(cnts)))

#drawing contours
for c in cnts:
    cv2.drawContours(img, [c], -1, (0,255,0), 2)


#cv2.imshow('mask', shape_mask)
cv2.imshow('image', img)
cv2.waitKey(0)