import numpy
import cv2
import numpy as np
import time
import sys
sys.path.append("../")
from decorators_folder.decorators import *

@debug
def preprocess(image):
    """
    convert the image from BGR to GRAYSCALE
    :param image:
    :return:
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray

@debug
def upscale(image, scale_factor):
    """
    upscales the size of the image to the desired scale factor
    :param image:
    :return:
    """
    h, w = image.shape
    newX = w * scale_factor
    newY = h * scale_factor
    upscalled = cv2.resize(image, (int(newX), int(newY)))
    return upscalled

@debug
def find_contours(image):
    """
    detect the edges of the image and draw them on black image and saves it
    :param image:
    :return:
    """
    edges = cv2.Canny(image, 60, 255)
    contours, hi = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(f'found {len(contours)} contours')
    print(contours[0])
    black_image = np.zeros_like(image)
    cv2.imshow('black', black_image)
    cv2.waitKey(0)
    cv2.drawContours(black_image, contours, -1, (255), 1)
    cv2.drawContours(image, contours, -1, (255), 1)
    cv2.imwrite(f'{int(time.time())}cont.jpg', black_image)
    cv2.imshow('cont', black_image)
    cv2.waitKey(0)
    cv2.imshow('cont', image)
    cv2.waitKey(0)
    cv2.imwrite(f'{int(time.time())}image.jpg', image)
    return black_image




