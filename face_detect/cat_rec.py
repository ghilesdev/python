#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 14:47:09 2020

@author: dev
"""




import argparse
import cv2



#parse arguments
ap=argparse.ArgumentParser()
ap.add_argument("-i","--image",required=True, help="path to image")
ap.add_argument("-c","--cascade",	default="haarcascade_frontalcatface.xml",
	help="path to cat detector haar cascade")
args=vars(ap.parse_args())


#load the image from arg
img=cv2.imread(args["image"])
gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#load the cat detector and detect cats
detector=cv2.CascadeClassifier(args["cascade"])

rects=detector.detectMultiScale(gray, scaleFactor=1.15, minNeighbors=10,
								minSize=(75, 75))

#draw rectangles
for (i,(x,y,w,h)) in enumerate(rects):
	cv2.rectangle(img, (x,y), (x+w,y+h), (0,0,255), 2)
	cv2.putText(img, 'Cat #{}'.format(i+1),(x,y-10), cv2.FONT_HERSHEY_SIMPLEX,
			 fontScale=1, color=(0,0,255))

cv2.imshow("img", img)
cv2.waitKey(0)



