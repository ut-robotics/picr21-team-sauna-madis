from image import *
from imageProcess import *

data = {
    "lH": 0,
    "lS": 0,
    "lV": 0,
    "hH": 0,
    "hS": 0,
    "hV": 0
    }

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


# window_processed = cv2.namedWindow("Processed")
# window_raw = cv2.namedWindow("RAW")
image = Image()
proccessed_ball = ImageProcess(70, 999999, "ball")

for key in data.keys():
    cv2.createTrackbar(key, "Processed", data[key], 255, eval("updateValue" + key))

while True:
    rawImage = image.get_rbg_image()
    proccessed_ball.find_objects(rawImage)
    #cv2.imshow(window_raw, rawImage)
    cv2.waitKey(1)
