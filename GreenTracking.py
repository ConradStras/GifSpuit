# import the neccesary packages
import cv2
import time
import numpy as np
import argparse
from collections import deque
import imutils
import WhiteLooping as wl
import time
import cython

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
                help="path to the (optional) video file")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
#comparison mask
greencompar = (20, 20, 20)
greencomparup = (64, 255, 255)

greenLower = (29, 84, 6)
greenUpper = (64, 255, 255)

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    camera = cv2.VideoCapture(0)

# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(args["video"])

# keep looping
while True:
    start_time = time.time()
    # grab the current frame
    (grabbed, frame) = camera.read()
    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if args.get("video") and not grabbed:
        break
    # color space
    frame = imutils.resize(frame, width=600)
    # rotating the video to see it properly
    (h, w) = frame.shape[:2]
    centerRot = (w / 2, h / 2)
    M = cv2.getRotationMatrix2D(centerRot, 180, 1.0)
    frame = cv2.warpAffine(frame, M, (w, h))
    # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    # I commented out the erode and dilate functions because it makes the green/white less visible
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    maskcompar = cv2.inRange(hsv, greencompar, greencomparup)
    # now to acquire the indexes of every green spot, read in order [y, x]
    indexes = wl.whiteindex(mask)
    clusters = wl.clusters(indexes, mask)
    for k in clusters:
        cv2.rectangle(frame, (k[0][1], k[0][0]), (k[1][1], k[1][0]), (255, 0, 0))
    cv2.line(frame, (0, int(h / 10)), (w, int(h / 10)), (0, 0, 255), 3)
    cv2.line(frame, (0, int(h * 9 / 10)), (w, int(h * 9 / 10)), (0, 0, 255), 3)
    # mask = cv2.erode(mask, None, iterations=2)
    # mask = cv2.dilate(mask, None, iterations=2)
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    cv2.imshow("Maskcompar", maskcompar)
    print("--- %s frames per seconds ---" % int(1 / (time.time() - start_time)))
    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
