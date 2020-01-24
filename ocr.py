#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 16:21:21 2020

@author: dev
"""

import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt 
'''
img=cv.imread('digits.png')
gray=cv.cvtColor(img, cv.COLOR_BGR2GRAY)

#split into rows and collumn
cells=[np.hsplit(row,100) for row in np.vsplit(gray, 50)]

#transform into array
x=np.array(cells)

#split into train and test data
trainData=x[:,:50].reshape(-1,400).astype(np.float32)
testData=x[:,50:100].reshape(-1,400).astype(np.float32)

k=np.arange(10)
train_labels=np.repeat(k,250)[:,np.newaxis]
test_labels=train_labels.copy()

#initiate knn
knn=cv.ml.KNearest_create()
knn.train(trainData,cv.ml.ROW_SAMPLE,train_labels)
ret, result, neigh, dist=knn.findNearest(testData, k=5)

matches =result==test_labels
correct=np.count_nonzero(matches)
accuracy=correct*100/result.size
print(accuracy)

#saving data
np.savez('knn_train_ocr.npz',trainData=trainData, train_labels=train_labels)
'''
#commented because data of training were saved
#now loading
with np.load('knn_train_ocr.npz') as data:
	print(data.files)
	trainData=data['trainData']
	train_labels=data['train_labels']
	
