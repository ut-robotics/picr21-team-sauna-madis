#HSV pilt

import pyrealsense2 as rs
import numpy as np
import cv2
params = cv2.SimpleBlobDetector_Params()
params.filterByArea = True
params.filterByCircularity = False
params.filterByConvexity = False
params.filterByInertia = False
params.minArea=500
params.maxArea=100000
detector = cv2.SimpleBlobDetector_create(params)

lH = 125
lS = 125
lV = 125
hH = 255
hS = 255
hV = 255


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



def updateValuelH(new_value):
    global lH
    lH = new_value
def updateValuelS(new_value):
    global lS
    lS = new_value
def updateValuelV(new_value):
    global lV
    lV = new_value
def updateValuehH(new_value):
    global hH
    hH = new_value
def updateValuehS(new_value):
    global hS
    hS = new_value
def updateValuehV(new_value):
    global hV
    hV = new_value
    
cv2.namedWindow("Processed")

cv2.createTrackbar("lH", "Processed", lH, 255, updateValuelH)
cv2.createTrackbar("lS", "Processed", lS, 255, updateValuelS)
cv2.createTrackbar("lV", "Processed", lV, 255, updateValuelV)
cv2.createTrackbar("hH", "Processed", hH, 255, updateValuehH)
cv2.createTrackbar("hS", "Processed", hS, 255, updateValuehS)
cv2.createTrackbar("hV", "Processed", hV, 255, updateValuehV)

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

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
        frame = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)



        lowerLimits = np.array([lH, lS, lV])
        upperLimits = np.array([hH, hS, hV])
        thresholded = cv2.inRange(frame, lowerLimits, upperLimits)
        
        outimage = cv2.bitwise_and(frame, frame, mask = thresholded)
        thresholded = cv2.bitwise_not(thresholded)
        keyPoints = detector.detect(thresholded)
        outimage = cv2.drawKeypoints(outimage, keyPoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        frame = cv2.drawKeypoints(frame, keyPoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        for keypoint in keyPoints:
            x=int(keypoint.pt[0])
            y=int(keypoint.pt[1])

            koord=(str(x)+":"+str(y))
            cv2.putText(frame, koord,(x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)

        #cv2.putText(frame, fps, (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2) fps jaoks ?

        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', frame)
        cv2.imshow('Processed', outimage)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
        
    tholder_new= open("trackbar_defaults.txt","w")
    tholder_new.write(str(lH)+"\n")
    tholder_new.write(str(lS)+"\n")
    tholder_new.write(str(lV)+"\n")
    tholder_new.write(str(hH)+"\n")
    tholder_new.write(str(hS)+"\n")
    tholder_new.write(str(hV)+"\n")

    tholder_new.close()
    # Stop streaming
    pipeline.stop()