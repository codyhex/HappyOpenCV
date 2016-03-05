# import the packages
import argparse
import imutils
import cv2

# argument parse for the image path
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="type in the input image path")
args = vars(ap.parse_args())

# load image, grayscale it and blur it
# the blur is used to filter out noise
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5,5), 0)          # a 5x5 kernel is applied
# use threshold to turn the image into a binary one
# if intensity of a pixel if larger than 60,
# replace the value with 255, which is white in OpenCV
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

# now find the contours
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]     # they change the position in OpenCV3

# process on each contour
for cnt in cnts:
    # computer center
    M = cv2.moments(cnt)
    cntX = int(M["m10"] / M["m00"])
    cntY = int(M["m01"] / M["m00"])

    # drawings
    cv2.drawContours(image, [cnt], -1, (0,255,0), 2)
    cv2.circle(image, (cntX,cntY), 5, (255,255,255), -1)
    cv2.putText(image, "center", (cntX - 20, cntY - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)

    # show results
    cv2.imshow("Find Contour Center", image)
    cv2.waitKey(0)
