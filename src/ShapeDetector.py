# this file holds the class of a shape detector, will will return the type of a given shape
import cv2

class ShapeDetector:
    def __init__(self):
        pass

    def detect(self, contour):
        # init the shape name and the approximated contour
        peri = cv2.arcLength(contour, True)
        # the approximated contour will reduce the points in the contour since we don't need them all
        # this method will find lines based on a length segment equal to 4% of the perimeter of the contour
        approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
        # it is easy to see how this works
        if len(approx) == 3:
            return "triangle"
        if len(approx) == 4:
            # compute the bounding box of the contour, judge the shape by edge ratio
            (x,y,w,h) = cv2.boundingRect(approx)
            ratio = w/float(h)
            return "square" if ratio > 0.95 and ratio < 1.05 else "rectangle"
        if len(approx) == 5:
            return "pentagon"
        else:
            return "circle"