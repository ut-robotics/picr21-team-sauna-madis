#HSV pilt

import pyrealsense2 as rs
import numpy as np
import cv2


#Data
cords = [0, 0]
depth = 0
def getCords():
    return cords
def getDepth():
    return depth

def loefaili(failinimi):
    try:
        with open(failinimi) as tholder:
            txtdata = tholder.readline()
            tykid = txtdata.split(",")
            vaartused = list(data.keys())

            for x in range(6):
                data[vaartused[x]] = int(tykid[x])
    except:
        print("Faili njetu")

#Detection
params = cv2.SimpleBlobDetector_Params()
params.filterByArea = True
params.filterByCircularity = False
params.filterByConvexity = False
params.filterByInertia = False
params.minArea=50
params.maxArea=100000
detector = cv2.SimpleBlobDetector_create(params)

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

#Threshold data
data = {
    "lH" : 0,
    "lS" : 0,
    "lV" : 0,
    "hH" : 0,
    "hS" : 0,
    "hV" : 0
}

#Loeb threshold data
loefaili("pall_defaults.txt")

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

config.enable_stream(rs.stream.depth, 640, 720, rs.format.z16, 30)

if device_product_line == 'L500':
    config.enable_stream(rs.stream.color, 960, 720, rs.format.bgr8, 30)
else:
    config.enable_stream(rs.stream.color, 640, 720, rs.format.bgr8, 30)
try:
    pipeline.stop()
except:
    print("camera oli juba stopped")


    
# Start streaming

#pipeline.start(config)  #õige asukoht

color_sensor = pipeline.start(config).get_device().query_sensors()[1]
color_sensor.set_option(rs.option.enable_auto_exposure, False)


def get_image(img):
    global depth

    try:
        #millist pilti
        if img == "Pall":
            loefaili("pall_defaults.txt")

        elif img == "Roosa":
            loefaili("roosa_defaults.txt")

        elif img == "Sinine":
            loefaili("sinine_defaults.txt")

        #pipeline.start(config)
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()

        #leiab depth pildi pealt kauguse meetrites, koordinaatidega (x,y)(hetkel ekraani keskelt), korvi kauguse mõõtmiseks
        distance = depth_frame.get_distance(320, 240)

        if distance > 0:
            #print("Kaugus:"+ str(distance))
            depth=distance

        color_image = np.asanyarray(color_frame.get_data())
        hsv = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)

        lowerLimits = np.array([data["lH"], data["lS"], data["lV"]])
        upperLimits = np.array([data["hH"], data["hS"], data["hV"]])
        thresholded = cv2.inRange(hsv, lowerLimits, upperLimits)

        outimage = cv2.bitwise_and(hsv, hsv, mask=thresholded)
        thresholded = cv2.bitwise_not(thresholded)
        keyPoints = detector.detect(thresholded)
        outimage = cv2.drawKeypoints(outimage, keyPoints, np.array([]), (0, 0, 255),
                                    cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        hsv = cv2.drawKeypoints(hsv, keyPoints, np.array([]), (0, 0, 255),
                                cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)


        # leida lähib keypoint ja lisada see cordsi. Lähib leida blob suuruse kaudu ?
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

        if len(keyPoints) == 0:
            cords.append(0)
            cords.append(0)
            cords.pop(0)
            cords.pop(0)

        # Show images, päris mängus ei ole vaja kuvada pilti
        #cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        #cv2.imshow('RealSense', thresholded)
        #cv2.waitKey(1)
    except:
        print("cameraerror")
#    finally:
 #       # Stop streaming
  #      pipeline.stop()