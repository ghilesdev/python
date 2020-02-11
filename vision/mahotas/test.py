from mahotas.features import surf
import matplotlib.pyplot as plt
from PIL import ImageEnhance, Image, ImageFilter, ImageOps
import cv2


image = Image.open("2.png")
# image = cv2.imread('2.png')
gray = ImageOps.grayscale(image)
# enh=ImageEnhance.Contrast(image)
# enh.enhance(1.3).show("30 percent more contrast")

im1 = gray.filter(ImageFilter.BLUR)
im2 = gray.filter(ImageFilter.CONTOUR)
im3 = gray.filter(ImageFilter.FIND_EDGES)

im4 = gray.filter(ImageFilter.DETAIL)
im5 = gray.filter(ImageFilter.EMBOSS)
im6 = gray.filter(ImageFilter.SHARPEN)

im7 = gray.filter(ImageFilter.SMOOTH)

im8 = gray.filter(ImageFilter.EDGE_ENHANCE)
im9 = gray.filter(ImageFilter.EDGE_ENHANCE_MORE)

# plt.subplot(2, 2, 1)
# plt.title('BLUR')
# plt.imshow(im1)
# plt.subplot(2, 2, 2)
# plt.title('CONTOUR')
# plt.imshow(im2)
# plt.subplot(2, 2, 3)
# plt.title('FIND EDGES')
# plt.imshow(im3)
# plt.subplot(2, 2, 4)
# plt.title('GRAY')
# plt.imshow(gray)
# plt.show()

plt.subplot(2, 2, 1)
plt.title("DETAIL")
plt.imshow(im4)
plt.subplot(2, 2, 2)
plt.title("EMBOSS")
plt.imshow(im5)
plt.subplot(2, 2, 3)
plt.title("SHARPEN")
plt.imshow(im6)
plt.subplot(2, 2, 4)
plt.title("SMOOTH")
plt.imshow(im7)
plt.show()
