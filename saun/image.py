#from tkinter import S
import pyrealsense2 as rs
import numpy as np
import cv2

class Image:

    def __init__(self):
        # Data
        self.aligned_depth_frame = 0
        self.depth = 0
        self.pipeline = None

        # Configure depth and color streams
        self.pipeline = rs.pipeline()

        self.config = rs.config()

        # Get device product line for setting a supporting resolution
        self.pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        self.pipeline_profile = self.config.resolve(self.pipeline_wrapper)
        self.device = self.pipeline_profile.get_device()
        self.device_product_line = str(self.device.get_info(rs.camera_info.product_line))
        print(self.device_product_line)

        found_rgb = False
        for s in self.device.sensors:
            if s.get_info(rs.camera_info.name) == 'RGB Camera':
                found_rgb = True
                break
        if not found_rgb:
            print("The demo requires Depth camera with Color sensor")
            exit(0)

        self.config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 60)
        self.config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 60)

#        self.pipeline.stop()
        #Start streaming
        """
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        OLD CODE IF NOT WORKING WITH UPDATE FIX OR UNCOMMENT
        ALSO CHANGE profile.set_... to color_sensor.set_...
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        """

        self.profile = self.pipeline.start(self.config)

        self.color_sensor = self.profile.get_device().query_sensors()[1]
        
        #self.profile = self.pipeline.start(self.config)

        self.color_sensor.set_option(rs.option.enable_auto_exposure, False)
        self.color_sensor.set_option(rs.option.enable_auto_white_balance, False)
        self.color_sensor.set_option(rs.option.white_balance, 3300)
        self.color_sensor.set_option(rs.option.exposure, 80)

        self.depth_sensor = self.profile.get_device().first_depth_sensor()
        self.depth_scale = self.depth_sensor.get_depth_scale()
        print("Depth Scale is: ", self.depth_scale)

        # We will be removing the background of objects more than
        #  clipping_distance_in_meters meters away
        self.clipping_distance_in_meters = 1  # 1 meter
        self.clipping_distance = self.clipping_distance_in_meters / self.depth_scale

        # Create an align object
        # rs.align allows us to perform alignment of depth frames to others frames
        # The "align_to" is the stream type to which we plan to align depth frames.
        self.align_to = rs.stream.color
        self.align = rs.align(self.align_to)

    def getDepth(self, x, y):
        return self.aligned_depth_frame.get_distance(x, y)

    def get_aligned_Frames(self):
        """
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        OLD CODE IF NOT WORKING WITH UPDATE FIX OR UNCOMMENT
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        frames = self.pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        self.depth_frame = frames.get_depth_frame()
        color_image = np.asanyarray(color_frame.get_data())
        hsv = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)
        """
        # Get frameset of color and depth
        frames = self.pipeline.wait_for_frames()
        # frames.get_depth_frame() is a 640x360 depth image

        # Align the depth frame to color frame
        aligned_frames = self.align.process(frames)

        # Get aligned frames
        aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
        color_frame = aligned_frames.get_color_frame()

        # Validate that both frames are valid
        if not aligned_depth_frame or not color_frame:
            print("Depth and color frames are not valid")
            return None

        return aligned_frames