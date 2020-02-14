#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 11:42:16 2019

@author: dev
"""

import matplotlib.pyplot as plt
import numpy as np
import cv2

from keras.applications import inception_v3

import time

# get the reference to the webcam
camera = cv2.VideoCapture(0)
camera_height = 500

while True:
    # read a new frame
    _, frame = camera.read()

    # flip the frameq
    frame = cv2.flip(frame, 1)

    # rescaling camera output
    aspect = frame.shape[1] / float(frame.shape[0])
    res = int(aspect * camera_height)  # landscape orientation - wide image
    frame = cv2.resize(frame, (res, camera_height))

    # add rectangle
    cv2.rectangle(frame, (300, 75), (650, 425), (240, 100, 0), 2)

    # get ROI
    roi = frame[75 + 2 : 425 - 2, 300 + 2 : 650 - 2]

    # parse BRG to RGB
    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)

    # resize to 224*224
    roi = cv2.resize(roi, (399, 399))
    roi = inception_v3.preprocess_input(roi)

    # predict!
    roi2 = np.array([cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)])

    predictions = model.predict(roi2)

    labels = inception_v3.decode_predictions(predictions, top=3)[0]

    # add text
    label_1 = "{} - {}%".format(labels[0][1], int(labels[0][2] * 100))
    cv2.putText(
        frame, label_1, (70, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (20, 240, 150), 2
    )

    # add text
    label_2 = "{} - {}%".format(labels[1][1], int(labels[1][2] * 100))
    cv2.putText(
        frame, label_2, (70, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (20, 240, 240), 2
    )

    # add text
    label_3 = "{} - {}%".format(labels[2][1], int(labels[2][2] * 100))
    cv2.putText(
        frame, label_3, (70, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (20, 20, 240), 2
    )

    # show the frame
    cv2.imshow("Real Time object detection", frame)

    key = cv2.waitKey(1)

    # quit camera if 'q' key is pressed
    if key & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
