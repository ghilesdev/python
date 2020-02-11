import cv2
import numpy as np

image = cv2.imread('2.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
canny = cv2.Canny(gray, 60, 150, apertureSize=3)

#hough line params
min_line_length = 100
max_line_gap = 10


hough_lines = cv2.HoughLinesP(canny, 1, np.pi/180, 100, minLineLength=min_line_length,
                              maxLineGap=max_line_gap)
black = np.zeros_like(image)
for x1, y1, x2, y2 in hough_lines[0]:
    cv2.line(black, (x1, y1), (x2, y2), (0,255,0), 1)


cv2.imshow('canny', canny)
cv2.imshow('hough', black)
cv2.waitKey(0)