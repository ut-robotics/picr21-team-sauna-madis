#HSV pilt
import keyboard
import pyrealsense2 as rs
import numpy as np
import cv2

params = cv2.SimpleBlobDetector_Params()
params.filterByArea = True
params.filterByCircularity = False
params.filterByConvexity = False
params.filterByInertia = False
params.minArea=50
params.maxArea=100000
detector = cv2.SimpleBlobDetector_create(params)


data = {
    "lH" : 0,
    "lS" : 0,
    "lV" : 0,
    "hH" : 0,
    "hS" : 0,
    "hV" : 0
}

try:
    with open("pall_defaults.txt") as tholder:
        txtdata = tholder.readline()
        tykid = txtdata.split(",")
        vaartused = list(data.keys())

        for x in range(6):
            data[vaartused[x]] = int(tykid[x])

except:
    print("Faili njetu")

def updateValuelH(new_value):
    global data
    data["lH"] = new_value
def updateValuelS(new_value):
    global data
    data["lS"] = new_value
def updateValuelV(new_value):
    global data
    data["lV"] = new_value
def updateValuehH(new_value):
    global data
    data["hH"] = new_value
def updateValuehS(new_value):
    global data
    data["hS"] = new_value
def updateValuehV(new_value):
    global data
    data["hV"] = new_value

def saveValue(fail):
    tholder_new = open(fail, "w")
    values = data.values()

    for value in values:
        cnt = 0
        if (cnt == 5):
            tholder_new.write(str(value))
        else:
            tholder_new.write(str(value) + ",")
        cnt += 1

    tholder_new.close()
    pass




cv2.namedWindow("Processed")

cv2.createTrackbar("lH", "Processed", data["lH"], 255, updateValuelH)
cv2.createTrackbar("lS", "Processed", data["lS"], 255, updateValuelS)
cv2.createTrackbar("lV", "Processed", data["lV"], 255, updateValuelV)
cv2.createTrackbar("hH", "Processed", data["hH"], 255, updateValuehH)
cv2.createTrackbar("hS", "Processed", data["hS"], 255, updateValuehS)
cv2.createTrackbar("hV", "Processed", data["hV"], 255, updateValuehV)


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
#pipeline.start(config)

color_sensor = pipeline.start(config).get_device().query_sensors()[1]
color_sensor.set_option(rs.option.enable_auto_exposure, False)
color_sensor.set_option(rs.option.enable_auto_white_balance, False)

try:
    while True:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())
        frame = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)

        lowerLimits = np.array([data["lH"], data["lS"], data["lV"]])
        upperLimits = np.array([data["hH"], data["hS"], data["hV"]])
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

        if keyboard.is_pressed("z"):
            saveValue("pall_defaults.txt")
            print("Salvestasin palli väärtused")
        elif keyboard.is_pressed("x"):
            saveValue("roosa_defaults.txt")
            print("Salvestasin roosa korvi väärtused")
        elif keyboard.is_pressed("c"):
            saveValue("sinine_defaults.txt")
            print("Salvestasin sinise korvi väärtused")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Stop streaming
    pipeline.stop()