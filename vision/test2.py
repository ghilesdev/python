from contour_finder import *
import cv2


if __name__ == "__main__":
    img = cv2.imread("1.png")
    cv2.imshow("frame", img)
    cv2.waitKey(0)
    preprocessed = preprocess(img)
    cv2.imshow("preprocessed", preprocessed)
    cv2.waitKey(0)
    upscalled = upscale(preprocessed, 2)
    cv2.imshow("upscalled", upscalled)
    cv2.waitKey(0)
    contours = find_contours(upscalled)
    cv2.imshow("final", contours)
    cv2.waitKey(0)
