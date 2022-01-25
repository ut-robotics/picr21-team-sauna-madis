import cv2
#from cv2 import WINDOW_NORMAL
#import cv2.cv2
import numpy as np
import time
from var import *

class ImageProcess:

    def __init__(self, minArea, maxArea, object):
        ##Data
        self.cords = [0,0]
        self.lower_limits = 0
        self.upper_limits = 0
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
        # What image
        print(object)
        if object == ImageProccesBall.OBJECT:
            for x in BallHL:
                self.data[x.name] = x.value
        elif object == BasketColor.PINK:
            for x in PinkBasketHL:
                self.data[x.name] = x.value
        elif object == BasketColor.BLUE:
            for x in BlueBasketHL:
                self.data[x.name] = x.value

        # Detection
        params = cv2.SimpleBlobDetector_Params()
        params.filterByArea = True
        params.filterByCircularity = False
        params.filterByConvexity = False
        params.filterByInertia = False
        minArea = int(minArea.value)
        maxArea = int(maxArea.value)
        params.minArea = minArea
        params.maxArea = maxArea
        self.detector = cv2.SimpleBlobDetector_create(params)
        print(self.data)
        self.lower_limits = np.array([self.data["lH"], self.data["lS"], self.data["lV"]])
        self.upper_limits = np.array([self.data["hH"], self.data["hS"], self.data["hV"]])

    def get_cords(self):
        return self.cords

    def show_image(self, window, image):
        cv2.imshow(window, image )
        cv2.waitKey(1)

    def find_objects(self, color_image, data):

        if data != None:
            self.data = data
            self.lower_limits = np.array([data["lH"], data["lS"], data["lV"]])
            self.upper_limits = np.array([data["hH"], data["hS"], data["hV"]])

        color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)

        start = time.time()
        fps = 1/(start - self.previous_time)
        self.previous_time = start

        thresholded = cv2.inRange(color_image, self.lower_limits, self.upper_limits)
        thresholded = cv2.bitwise_not(thresholded)
        
        outputImage = cv2.copyMakeBorder(thresholded, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=[255, 255, 255])
        
        kernel = np.ones((5,5), np.uint8)
        outputImageFiltered = cv2.medianBlur(outputImage, 3)
        outputImageFiltered = cv2.dilate(outputImage, kernel, iterations=1)
        outputImageFiltered = cv2.erode(outputImage, kernel, iterations=2)
        
        keyPoints = self.detector.detect(outputImageFiltered)

        outimage = cv2.drawKeypoints(outputImageFiltered, keyPoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        cv2.putText(outimage, str(round(fps)), (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        hsv = cv2.drawKeypoints(color_image, keyPoints, np.array([]), (0, 0, 255),cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
       
       
        # Finds keypoints
        self.cords.clear()
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

        
        sorted(self.cords, key = lambda ball_y: ball_y[1], reverse = True)
        #Show images
        
        cv2.namedWindow("Processed image", cv2.WINDOW_AUTOSIZE)
        cv2.imshow("Processed image", outimage)
        cv2.waitKey(1)
        #self.show_image(window, self.hsv)

        #return self.outimage


