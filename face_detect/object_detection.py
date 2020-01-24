#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 20:05:02 2020

@author: dev
"""

from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time


#parse arguments
ap=argparse.ArgumentParser()
ap.add_argument("-v","--video",help="path to video")
ap.add_argument("-b","--buffer",type=int, default=64,help="max buffer size")
args=vars(ap.parse_args())

#define lower and upper boundaries for color detect
green_lower=(29,86,6)
green_upper=(64,255,255)

#max length of the trail
pts=deque(maxlen=args["buffer"])

#if no video file, access to the webcam
if not args.get("video", False):
	vs=VideoStream(src=0).start()
else:
	vs=cv2.VideoCapture(args["video"])

time.sleep(1.0)

while True:
	frame=vs.read()
	frame=frame[1] if args.get("video", False) else frame
	if frame is None:
		break
	#resizing img, blurring, converting color
	frame=imutils.resize(frame, width=600)
	blurred=cv2.GaussianBlur(frame, (11,11),0)
	hsv=cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
	
	#constructing a mask, followed by a series of dilatations/errosion
	mask=cv2.inRange(hsv, green_lower,green_upper)
	mask=cv2.erode(mask, None, iterations=2)
	mask=cv2.dilate(mask, None, iterations=2)
	
	#finding countours
	cnts=cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, 
					   cv2.CHAIN_APPROX_SIMPLE)
	cnts=imutils.grab_contours(cnts)
	center=None
	
	#if contour found
	if len(cnts)>0:
		#finding the largest contour
		c=max(cnts, key=cv2.contourArea)
		((x,y),radius)=cv2.minEnclosingCircle(c)
		M=cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		
		if radius > 10:
			#draw the circle then the trail
			cv2.circle(frame, (int(x),int(y)), int(radius), (0,255,255),2)
			cv2.circle(frame, center, 5, (0,0,255), -1)
			
		pts.appendleft(center)
		
	for i in range(1,len(pts)):
		#if either of the points is none, ignore it
		if pts[i-1] is None or pts[i] is None:
			continue
		#otherwise, calculate thickness of the line and draw
		thick=int(np.sqrt(args["buffer"]/float(i+1))*2.5)
		cv2.line(frame, pts[i-1], pts[i], (0,255,255), thick)
	
	#rendering the frame
	cv2.imshow("Frame", frame)
	key=cv2.waitKey(1) & 0xFF
	
	#if q is pressed, stop the loop
	if key== ord('q'):
		break
	
#if we are not using a video, close the stream 
if not args.get("video", False):
	vs.stop()
	
else:
	#else stop the webcam
	vs.release()
	
#close all windows
cv2.destroyAllWindows()


