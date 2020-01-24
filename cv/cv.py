import numpy as np
import cv2

'''
def do_nothing(x):
    return None


cap = cv2.VideoCapture(0)
# create window for trackbars
cv2.namedWindow('thres')
# create trackbars
cv2.createTrackbar('low_thres', 'thres', 0, 255, do_nothing)
cv2.createTrackbar('high_thres', 'thres', 0, 255, do_nothing)

while True:
    #getting values from trackbars
    low = cv2.getTrackbarPos('low_thres', 'thres')
    high = cv2.getTrackbarPos('high_thres', 'thres')

    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # gray=cv2.rectangle(gray,(50,50),(200,200),(0,255,0),3)
    canny = cv2.Canny(gray, low, high)

    cv2.imshow('frame_grayscale', canny)
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
'''


img=cv2.imread('picture.jpg')
img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

gray=np.float32(img)
dst=cv2.cornerHarris(gray,2,3,0.04)

dst=cv2.dilate(dst, None)
print(dst.max() )
#img[dst>0.01*dst.max()]=[0,0,255]
cv2.imshow('window', dst)
if cv2.waitKey(0) & 0xFF == ord('q'):
    cv2.destroyAllWindows()
