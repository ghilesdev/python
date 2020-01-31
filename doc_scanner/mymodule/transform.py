import numpy as np
import cv2


def order_points(pts):
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype='float32')

    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect


def four_points_transform(image, pts):
    # obtain a consistent order of the points and unpack them
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    # calculate the width of the new image that will be the max distance on x-axis between
    # the tl point and tr, and between br and bl point
    widthA = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    widthB = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    max_width = max(int(widthA), int(widthB))

    # calculate the height of the new image that will be the max distance on y-axis between
    # the tl point and bl, and between tr and br point
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    max_height = max(int(heightA), int(heightB))

    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst=np.array([
        [0,0],
        [max_width-1, 0],
        [max_width, max_height],
        [0, max_height-1]
    ], dtype='float32')

    #compute the perspective transform matrix
    M=cv2.getPerspectiveTransform(rect, dst)
    warped=cv2.warpPerspective(image, M, (max_width, max_height))

    return warped


