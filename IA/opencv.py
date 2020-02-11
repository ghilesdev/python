import matplotlib.pyplot as plt
import cv2
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter


cl1 = [255, 0, 0]
cl2 = [0, 255, 0]
cl3 = [0, 0, 255]
alp = [127, 127, 127]
plt.imshow(np.array([[cl1, cl2], [cl3, alp]]))
