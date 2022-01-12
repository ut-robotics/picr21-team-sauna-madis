#Imports
import pyrealsense2 as rs
import numpy as np
import cv2

####Data
cords = [0, 0]
depth_frame= 0
depth = 0
pinkBasket = (66,125,181,182,218,255)
blueBasket = (108,53,70,155,131,143)
ball = (14,44,79,145,255,188)
xDepth = 320
yDepth = 240

#Threshold data
data = {
    "lH" : 0,
    "lS" : 0,
    "lV" : 0,
    "hH" : 0,
    "hS" : 0,
    "hV" : 0
}

#Functions
def getCords():
    return cords

def getDepth(x, y):
    global depth_frame
    depth =  depth_frame.get_distance(x, y)
    return depth

def readThresHold(img):
    keys = list(data.keys())
    #What image
    if img == "ball":
        for x in range(6):
            data[keys[x]] = ball[x]
        print(data)
    elif img == "pink":
        for x in range(6):
            data[keys[x]] = pinkBasket[x]
    elif img == "blue":
        for x in range(6):
            data[keys[x]] = blueBasket[x]



#Detection
params = cv2.SimpleBlobDetector_Params()
params.filterByArea = True
params.filterByCircularity = False
params.filterByConvexity = False
params.filterByInertia = False
params.minArea=50
params.maxArea=9999999
detector = cv2.SimpleBlobDetector_create(params)

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))
print(device_product_line)

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
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
else:
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
try:
    pipeline.stop()
except:
    print("camera oli juba stopped")


    
# Start streaming

#pipeline.start(config)  #õige asukoht

color_sensor = pipeline.start(config).get_device().query_sensors()[1]
color_sensor.set_option(rs.option.enable_auto_exposure, False)
color_sensor.set_option(rs.option.enable_auto_white_balance, False)

def get_image(img):
    global depth, depth_frame

    try:
        #Reads threshold data
        readThresHold(img)
        #pipeline.start(config)
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()

        #Finds dept
        distance = depth_frame.get_distance(320, 240)

        if distance > 0:
            depth=distance

        color_image = np.asanyarray(color_frame.get_data())
        hsv = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)

        lowerLimits = np.array([data["lH"], data["lS"], data["lV"]])
        upperLimits = np.array([data["hH"], data["hS"], data["hV"]])
        thresholded = cv2.inRange(hsv, lowerLimits, upperLimits)

        outimage = cv2.bitwise_and(hsv, hsv, mask=thresholded)
        thresholded = cv2.bitwise_not(thresholded)
        outputImage = cv2.copyMakeBorder(thresholded, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=[255,255,255])
        keyPoints = detector.detect(outputImage)
        outimage = cv2.drawKeypoints(outputImage, keyPoints, np.array([]), (0, 0, 255),
                                    cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        hsv = cv2.drawKeypoints(hsv, keyPoints, np.array([]), (0, 0, 255),
                                cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)


        #Finds keypoints
        for keypoint in keyPoints:
            x = int(keypoint.pt[0])
            y = int(keypoint.pt[1])
            #Saves keypoints
            cords.append(x)
            cords.append(y)
            cords.pop(0)
            cords.pop(0)

            koord = (str(x) + ":" + str(y))
            cv2.putText(hsv, koord, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)

        if len(keyPoints) == 0:
            cords.append(0)
            cords.append(0)
            cords.pop(0)
            cords.pop(0)

        #Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', outputImage)
        cv2.waitKey(1)
    except:
        print("cameraerror")