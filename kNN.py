#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 15:14:21 2020

@author: dev
"""
# classification

import numpy as np
import cv2
from matplotlib import pyplot as plt

trainData = np.random.randint(0, 100, (25, 2)).astype(np.float32)

responses = np.random.randint(0, 2, (25, 1)).astype(np.float32)
red = trainData[responses.ravel() == 0]
plt.scatter(red[:, 0], red[:, 1], 80, "r", "^")

blue = trainData[responses.ravel() == 1]
plt.scatter(blue[:, 0], blue[:, 1], 80, "b", "s")


newcomer = np.random.randint(0, 100, (1, 2)).astype(np.float32)
plt.scatter(newcomer[:, 0], newcomer[:, 1], 80, "g", "o")


"""knn=cv2.KNearest()
knn.train(training_data,cv2.ml.ROW_SAMPLE ,respone)
ret, results, neighbours, dist=knn.find_nearest(new_comer,3)"""

knn = cv2.ml.KNearest_create()
knn.train(trainData, cv2.ml.ROW_SAMPLE, responses)
ret, results, neighbours, dist = knn.findNearest(newcomer, k=3)

print("results", results)
print("neighbours: ", neighbours)
print("distance: ", dist)
plt.show()
