#HSV pilt

import pyrealsense2 as rs
import numpy as np
import cv2

#Data
cords = [0,0]

def getCords():
    return cords
#Detection
params = cv2.SimpleBlobDetector_Params()
params.filterByArea = True
params.filterByCircularity = False
params.filterByConvexity = False
params.filterByInertia = False
params.minArea=500
params.maxArea=100000
detector = cv2.SimpleBlobDetector_create(params)

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

#Loeb threshold data
try:
    with open("trackbar_defaults.txt") as tholder:
        lH = int(tholder.readline())
        lS = int(tholder.readline())
        lV = int(tholder.readline())
        hH = int(tholder.readline())
        hS = int(tholder.readline())
        hV = int(tholder.readline())
except:
    print("Faili njetu")

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break
if not found_rgb:
    print("The demo requires Depth camera with Color sensor")
    exit(0)

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

if device_product_line == 'L500':
    config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
else:
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

try:
    while True:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())
        hsv = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)

        lowerLimits = np.array([lH, lS, lV])
        upperLimits = np.array([hH, hS, hV])
        thresholded = cv2.inRange(hsv, lowerLimits, upperLimits)

        outimage = cv2.bitwise_and(hsv, hsv, mask=thresholded)
        thresholded = cv2.bitwise_not(thresholded)
        keyPoints = detector.detect(thresholded)
        outimage = cv2.drawKeypoints(outimage, keyPoints, np.array([]), (0, 0, 255),
                                     cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        hsv = cv2.drawKeypoints(hsv, keyPoints, np.array([]), (0, 0, 255),
                                  cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        for keypoint in keyPoints:
            x = int(keypoint.pt[0])
            y = int(keypoint.pt[1])
            #Salvestan koordinaadid kui need pole 0 ?
            cords.append(x)
            cords.append(y)
            cords.pop(0)
            cords.pop(0)

            koord = (str(x) + ":" + str(y))
            cv2.putText(hsv, koord, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)

        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', hsv)
        cv2.waitKey(1)

finally:

    # Stop streaming
    pipeline.stop()