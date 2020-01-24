#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 25 19:08:58 2018

@author: dev
"""

import cv2
import numpy as np
h,s,v=0,0,0

width=640
height=480
max_obj=50
min_obj_area=20*20
max_obj_area=width*height/1.5
wind_name1="original"
wind_name2="hsv"
wind_name3="thres"
wind_name4="morpho"
wind_trackbar="trackbar"

def on_trackbar(x):
    pass

def create_trackbar():

    cv2.namedWindow('image')

    # create trackbars for color change
    cv2.createTrackbar('h','image',0,255,on_trackbar)
    cv2.createTrackbar('s','image',0,255,on_trackbar)
    cv2.createTrackbar('v','image',0,255,on_trackbar)
    while(1):
        #cv2.imshow('image',img)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

        # get current positions of four trackbars
        h = cv2.getTrackbarPos('h','image')
        s = cv2.getTrackbarPos('s','image')
        v = cv2.getTrackbarPos('v','image')




    cv2.destroyAllWindows()
    pass

def draw_object(x,y,frame):
    cv2.circle(frame,(x,y),20,(0,255,0),2)
    if(y-25>0):
        cv2.line(frame(x,y),(x,y-25),(0,255,0),2)
    else:
        cv2.line(frame,(x,y),(x,0),(0,255,0),2)
    if(y+25<height):
        cv2.line(frame,(x,y),(x,y+25),(0,255,0),2)
    else:
        cv2.line(frame,(x,y),(x,height),(0,255,0),2)
    if(x-25>0):
        cv2.line(frame,(x,y),(x-25,y),(0,255,0),2)
    else:
        cv2.line(frame,(x,y),(0,y),(0,255,0),2)
    if(x+25<width):
        cv2.line(frame,(x,y),(x+25,y),(0,255,0),2)
    else:
        cv2.line(frame,(x,y),(width,y),(0,255,0),2)
    cv2.putText(frame,str(x)+","+str(y),(x,y+30),1,1,(0,255,0),2)
    pass

def morphOps(thresh):
    erodeElement=cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
    dilateElement=cv2.getStructuringElement(cv2.MORPH_RECT,(8,8))
    cv2.erode(thresh,thresh,erodeElement)
    cv2.erode(thresh,thresh,erodeElement)

    cv2.dilate(thresh,thresh,dilateElement)
    cv2.dilate(thresh,thresh,dilateElement)

    pass

def trackFilteredObject(x,y,threshold,cameraFeed):
    temp=np.copy(threshold)
    ret,thresh = cv2.threshold(temp,127,255,0)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if (hierarchy.size() > 0):
        numObjects=hierarchy.size()
    cnt = contours[0]
    M = cv2.moments(cnt)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    pass

create_trackbar()
cap = cv2.VideoCapture(0)
while(True):
    ret, frame = cap.read()
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frame_threshold = cv.inRange(frame_hsv, (h,s,v), (h,s,v))
    if(useMorphOps):
        morphOps(threshold)
    if(trackObjects):
        trackFilteredObject(x,y,threshold,cap)
    cv2.imshow(windowName3,threshold)
	cv2.imshow(windowName1,cap)
	cv2.imshow(windowName2,hsv)
    cv2.waitKey(30)
