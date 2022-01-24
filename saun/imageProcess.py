import cv2
from cv2 import WINDOW_NORMAL
#import cv2.cv2
import numpy as np
import time

class ImageProcess:
    #Data
    pinkBasket = (170,183,187,178,255,255)
    blueBasket = (107,237,91,123,255,153)
    ball = (13,136,37,85,255,153)

    def __init__(self, minArea, maxArea, object):
        ##Data
        self.cords = []
        self.lowerLimits = 0
        self.upperLimits = 0
        self.dectector = 0
        self.previous_time = 0
        self.outimage = 0

        self.data = {
            "lH": 0,
            "lS": 0,
            "lV": 0,
            "hH": 0,
            "hS": 0,
            "hV": 0
        }

        keys = list(self.data.keys())
        # What image
        if object == "ball":
            for x in range(6):
                self.data[keys[x]] = self.ball[x]
        elif object == "pink":
            for x in range(6):
                self.data[keys[x]] = self.pinkBasket[x]
        elif object == "blue":
            for x in range(6):
                self.data[keys[x]] = self.blueBasket[x]

        # Detection
        params = cv2.SimpleBlobDetector_Params()
        params.filterByArea = True
        params.filterByCircularity = False
        params.filterByConvexity = False
        params.filterByInertia = False
        params.minArea = minArea
        params.maxArea = maxArea
        self.detector = cv2.SimpleBlobDetector_create(params)

        self.lowerLimits = np.array([self.data["lH"], self.data["lS"], self.data["lV"]])
        self.upperLimits = np.array([self.data["hH"], self.data["hS"], self.data["hV"]])

    def getcords(self):
        return self.cords

    def show_image(self, window, image):
        cv2.imshow(window, image )
        cv2.waitKey(1)

    def find_objects(self, color_image, data):

        if data != None:
            self.data = data

        color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)

        start = time.time()
        fps = 1/(start - self.previous_time)
        self.previous_time = start

        thresholded = cv2.inRange(color_image, self.lowerLimits, self.upperLimits)
        thresholded = cv2.bitwise_not(thresholded)
        outputImage = cv2.copyMakeBorder(thresholded, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=[255, 255, 255])
        kernel = np.ones((5,5), np.uint8)
        outputImageFiltered = cv2.medianBlur(outputImage, 3)
        outputImageFiltered = cv2.dilate(outputImage, kernel, iterations=1)
        outputImageFiltered = cv2.erode(outputImage, kernel, iterations=2)
        keyPoints = self.detector.detect(outputImageFiltered)
        outimage = cv2.drawKeypoints(outputImageFiltered, keyPoints, np.array([]), (0, 0, 255),
                                     cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        cv2.putText(outimage, str(round(fps)), (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        hsv = cv2.drawKeypoints(color_image, keyPoints, np.array([]), (0, 0, 255),
                                cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        self.cords.clear()
        # Finds keypoints
        for keypoint in keyPoints:
            ball_keypoints = []
            x = int(keypoint.pt[0])
            y = int(keypoint.pt[1])
            # Saves keypoints

            ball_keypoints.append(x)
            ball_keypoints.append(y)

            self.cords.append(ball_keypoints)

            koord = (str(x) + ":" + str(y))
            cv2.putText(hsv, koord, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)

        if len(keyPoints) == 0:
            self.cords.append([0,0])

        
        sorted(self.cords, key = lambda x: x[1], reverse = True)
        #Show images
        
        cv2.namedWindow("Processed image", cv2.WINDOW_AUTOSIZE)
        cv2.imshow("Processed image", outimage)
        cv2.waitKey(1)
        #self.show_image(window, self.hsv)

        #return self.outimage


