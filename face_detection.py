#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 17:19:18 2020

@author: dev
"""

import cv2

face=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

cap=cv2.VideoCapture(0)

while True:
	ret, frame=cap.read()
	if ret==True:
		gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	
		faces=face.detectMultiScale(gray, 1.1, 4)
	
		for(x,y,w,h)in faces:
			cv2.rectangle(frame, (x,y), (x+w,y+h),(0,255,127),2)
			cv2.imshow('faces', frame)
		k=(cv2.waitKey(30) & 0xff)
		if k==27:
			break
	else:
		print('error initializing camera')