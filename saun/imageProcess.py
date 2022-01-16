import cv2
import numpy as np

class imageProcess:
    ##Data
    cords = [0, 0]
    pinkBasket = (66,125,181,182,218,255)
    blueBasket = (108,53,70,155,131,143)
    ball = (14,44,79,103,255,188)
    lowerLimits = 0
    upperLimits = 0
    dectector = 0

    # Threshold data
    data = {
        "lH": 0,
        "lS": 0,
        "lV": 0,
        "hH": 0,
        "hS": 0,
        "hV": 0
    }

    def __init__(self, minArea, maxArea, object):
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

    def find_objects(self, rbgImage):
        try:
            thresholded = cv2.inRange(rbgImage, self.lowerLimits, self.upperLimits)

            outimage = cv2.bitwise_and(rbgImage, rbgImage, mask=thresholded)
            thresholded = cv2.bitwise_not(thresholded)
            outputImage = cv2.copyMakeBorder(thresholded, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=[255, 255, 255])
            keyPoints = self.detector.detect(outputImage)
            outimage = cv2.drawKeypoints(outputImage, keyPoints, np.array([]), (0, 0, 255),
                                         cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            hsv = cv2.drawKeypoints(rbgImage, keyPoints, np.array([]), (0, 0, 255),
                                    cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

            self.cords.clear()
            # Finds keypoints
            for keypoint in keyPoints:
                x = int(keypoint.pt[0])
                y = int(keypoint.pt[1])
                # Saves keypoints
                self.cords.append(x)
                self.cords.append(y)

                koord = (str(x) + ":" + str(y))
                cv2.putText(hsv, koord, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)

            if len(keyPoints) == 0:
                self.cords.append(0)
                self.cords.append(0)

            #Show images
            cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('RealSense', outimage)
            cv2.waitKey(1)

        except:
            print("cameraerror")


