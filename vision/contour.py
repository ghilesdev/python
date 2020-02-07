
# Find contours at a constant value of 0.8
import cv2 
import numpy as np 
import matplotlib.pyplot as plt
from tekyntools.geometryObjects.polyline import Polyline
from tekyntools.dxfTools.dxfWriter import listPolylineToDxf

# Let's load a simple image with 3 black squares 
image = cv2.imread("C:\\Users\\alaa\\Desktop\\image source\\4.png") 
 
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
height, width = gray.shape
# imgScale = 1
# newX,newY = width*imgScale, height*imgScale
# gray   = cv2.resize(gray,(int(newX),int(newY)))
# image   = cv2.resize(image,(int(newX),int(newY)))
def covertSobel(sobel):
    newSobel = np.zeros_like(sobel)
    for idx0,i in enumerate(sobel):
        for idx,j in enumerate(i) :
            if j!= 0:      
                newSobel[idx0][idx] = 255
    return newSobel

# sobelx = cv2.Sobel(gray,cv2.CV_64F,1,0,ksize=5) 
# sobely = cv2.Sobel(gray,cv2.CV_64F,0,1,ksize=5) 
# sobelx = covertSobel(sobelx)
# sobely = covertSobel(sobely)

# laplacian = cv2.Laplacian(gray,cv2.CV_64F) 
fig, ax = plt.subplots()
ax.imshow(dst, cmap=plt.cm.gray)
plt.show()



image1 = np.zeros_like(gray)
# Grayscale 

  
# Find Canny edges 
edged = cv2.Canny(sobelx, 30, 200) 
fig, ax = plt.subplots()
ax.imshow(edged, cmap=plt.cm.gray)
plt.show()


  
# Finding Contours 
# Use a copy of the image e.g. edged.copy() 
# since findContours alters the image 
contours, hierarchy = cv2.findContours(edged,  
    cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
    




cc=[]

for j in contours:
    c = []
    p=Polyline()
    

    for k in j :
        c.append(tuple(map(tuple,k))[0])
    
    p = p.listToPolyline(c)
  
    cc.append(p)
    print(type(p))


listPolylineToDxf(cc, path= r"contours"+".dxf", reverse=False)


  
print("Number of Contours found = " + str(len(contours))) 
  
# Draw all contours 
# -1 signifies drawing all contours 
cv2.drawContours(image1, contours, -1, (255, 0, 0), 1) 
  
# cv2.imshow('Contours', image1) 
# 
# cv2.destroyAllWindows() 




fig, ax = plt.subplots()
ax.imshow(image1, cmap=plt.cm.gray)
plt.show()
