# in order to make the folder visible, you have to place a "__init__.py" there
from ShapeDetector import ShapeDetector
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
resized = imutils.resize(image, width =300)
ratio = image.shape[0]/float(resized.shape[0])  #why init this?

gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5,5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
sd = ShapeDetector()

# loop through all detected contours
for c in cnts:
    M = cv2.moments(c)
    cX = int((M["m10"] / M["m00"]) * ratio)
    cY = int((M["m01"] / M["m00"]) * ratio)
    shape = sd.detect(c)

    # multiplay the contour by resized ration and draw them back
    c *= int(ratio)
    cv2.drawContours(image, [c], -1, (0,255,0),2)
    cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255,255,255), 2)

    # show the result
    cv2.imshow("Result", image)
    cv2.waitKey(0)
