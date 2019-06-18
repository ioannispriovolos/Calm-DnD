# import the necessary packages
from imutils.video import VideoStream
import datetime
import argparse
import imutils
import time
import cv2
import numpy as np
import random

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())

# initialize the video stream and allow the cammera sensor to warmup
vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution = (440, 480)).start()
time.sleep(2.0)

hobgoblin = cv2.imread('/home/pi/Desktop/hobgoblin.jpg', 1)
orc = cv2.imread('/home/pi/Desktop/orc.jpg', 1)

lower_range = {'red':(166, 84, 141), 'green':(66, 122, 129)}
upper_range = {'red':(186,255,255), 'green':(78, 255, 255)}

colors = {'red':(0,0,255), 'green':(0,255,0)}

# loop over the frames from the video stream
while True:

    frame = vs.read()

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    frame_h, frame_w, frame_c = frame.shape

    # white with 4 channels BGR and Alpha
    white = np.zeros((frame_h, frame_w, 4), dtype='uint8')
    white.fill(255)

    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    file_attackFrom = "/home/pi/Desktop/Python/attackFrom.txt"
    lines_attackFrom = open(file_attackFrom).read().splitlines()

    for attackFrom in range(len(lines_attackFrom)):

        linesx_attackFrom = (int(lines_attackFrom[attackFrom][6]) * 45) + 20
        linesy_attackFrom = (int(lines_attackFrom[attackFrom][14]) * 60) + 20

        x_from = int(lines_attackFrom[attackFrom][6])
        y_from = int(lines_attackFrom[attackFrom][14])

        point_attackFrom = (linesx_attackFrom, linesy_attackFrom)

    file_attackTo = "/home/pi/Desktop/Python/attackTo.txt"
    lines_attackTo = open(file_attackTo).read().splitlines()

    for attackTo in range(len(lines_attackTo)):

        linesx_attackTo = (int(lines_attackTo[attackTo][6]) * 45) + 20
        linesy_attackTo = (int(lines_attackTo[attackTo][14]) * 60) + 20

        x_to = int(lines_attackTo[attackTo][6])
        y_to = int(lines_attackTo[attackTo][14])

        point_attackTo = (linesx_attackTo, linesy_attackTo)

    x_m = linesx_attackTo - linesx_attackFrom
    y_m = linesy_attackTo - linesy_attackFrom

    if x_m != 0:
        y_final = round((y_m / x_m) * 10)
    elif x_m == 0:
        y_final = 30
        x_final = 30

    if y_m != 0:
        x_final = round((x_m / y_m) * 10)
    elif y_m == 0:
        x_final = 30
        y_final = 30

    cv2.line(white, (linesx_attackFrom, linesy_attackFrom), (linesx_attackFrom + x_final, linesy_attackFrom + y_final), (0,0,0), 5)

    if x_from < x_to and y_from < y_to and linesx_attackFrom < linesx_attackTo:
        linesx_attackFrom += x_final;
        linesy_attackFrom += y_final;
    elif x_from > x_to and y_from < y_to and linesy_attackFrom < linesy_attackTo:
        linesx_attackFrom += x_final;
        linesy_attackFrom -= y_final;
    elif x_from < x_to and y_from > y_to and linesx_attackFrom < linesx_attackTo:
        linesx_attackFrom -= x_final;
        linesy_attackFrom += y_final;
    elif x_from > x_to and y_from > y_to and linesx_attackFrom > linesx_attackTo:
        linesx_attackFrom -= x_final;
        linesy_attackFrom -= y_final;
    elif x_from == x_to and y_from < y_to and linesy_attackFrom < linesy_attackTo:
        linesy_attackFrom += y_final;
    elif y_from == y_to and x_from < x_to and linesx_attackFrom < linesx_attackTo:
        linesx_attackFrom += x_final;
    elif y_from == y_to and x_from > x_to and linesx_attackFrom > linesx_attackTo:
        linesx_attackFrom -= x_final;
    elif x_from == x_to and y_from > y_to and linesy_attackFrom > linesy_attackTo:
        linesy_attackFrom -= y_final;

    for key, value in upper_range.items():

        kernel = np.ones((9,9),np.uint8)
        mask = cv2.inRange(hsv, lower_range[key], upper_range[key])
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        # only proceed if at least one contour was found
        if len(cnts) > 0.01:
                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and
                # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            center_x = int(M["m10"] / M["m00"])
            center_y = int(M["m01"] / M["m00"])

    white = cv2.cvtColor(white, cv2.COLOR_BGR2BGRA)
    frame_h, frame_w, frame_c = white.shape

    file_monsters = "/home/pi/Desktop/Python/monsters.txt"
    lines_monsters = open(file_monsters).read().splitlines()

    for monsters in range(len(lines_monsters)):

        linesx_monster = (int(lines_monsters[monsters][6]) * 45)
        linesy_monster = (int(lines_monsters[monsters][14]) * 60)
        linesz_monster = lines_monsters[monsters][23]
        #print(linesz_monster)

        point_monster = (linesx_monster, linesy_monster)
        if linesz_monster == 'H':
            watermark = cv2.cvtColor(hobgoblin, cv2.COLOR_BGR2BGRA)
        elif linesz_monster == 'O':
            watermark = cv2.cvtColor(orc, cv2.COLOR_BGR2BGRA)
		# overlay with 4 channels BGR and Alpha
        overlay = np.zeros((frame_h, frame_w, 4), dtype='uint8')
        watermark_h, watermark_w, watermark_c = watermark.shape

        # replace overlay pixels with watermark pixel values
        for i in range(0, watermark_h):
            for j in range(0, watermark_w):
                if watermark[i,j][3] != 0:
                    offset = 10
                    h_offset = linesy_monster
                    w_offset = linesx_monster
                    white[h_offset + i, w_offset+ j] = watermark[i,j]

        cv2.addWeighted(overlay, 1.0, white, 1.0, 0, white)

    white = cv2.cvtColor(white, cv2.COLOR_BGRA2BGR)

    # show the frame
    cv2.imshow("Frame", white)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
            break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
