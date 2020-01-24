import cv2
import numpy as np
from matplotlib import pyplot as plt

def average_slop_intercep(image,lines):
    leftfit=[]
    rightfit=[]
    for line in lines:
        x1,y1,x2,y2=line.reshape(4)
        param=np.polyfit((x1,x2),(y1,y2),1)
        print(param)
        slop=param[0]
        inter=param[1]
        if slop
def canny(image):
    gs=cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    blur=cv2.GaussianBlur(gs,(5, 5),0)
    # détection de countour (source, gradient min, gradient max)
    canny= cv2.Canny(blur,50,150)
    return canny
def disp(image,lines):
    lane_image=np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1,y1,x2,y2=line.reshape(4)
            cv2.line(lane_image,(x1,y1),(x2,y2), (255,0,0),5)
    return lane_image

# creation d'un masque
def rOI(image):
    height=image.shape[0]
    poly=np.array([[(200,height),(1100,height),(550,250)]])
    mask=np.zeros_like(image)
    cv2.fillPoly(mask,poly,255)
    masked=cv2.bitwise_and(image, mask)
    return masked

image =cv2.imread('test_image.jpg')
lane_image=np.copy(image)

canny_image=canny(lane_image)
cropped=rOI(canny_image)
lines=cv2.HoughLinesP(cropped,2,np.pi/180,100,np.array([]),minLineLength=40, maxLineGap=5)
averaged_lines=average_slop_intercep(lane_image,lines)
line_image=disp(lane_image,lines)
added=cv2.addWeighted(lane_image,0.8,line_image,1,1)
cv2.imshow("result",added)
cv2.waitKey(0)
