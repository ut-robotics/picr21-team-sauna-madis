#from tkinter import S
import pyrealsense2 as rs
import numpy as np
import cv2

class Image:

    def __init__(self):
        # Data
        self.depth_image = None
        self.depth = 0
        self.pipeline = None

        # Configure depth and color streams
        self.pipeline = rs.pipeline()

        config = rs.config()

        # Get device product line for setting a supporting resolution
        pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
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

        config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 60)
        config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 60)

#        self.pipeline.stop()
        #Start streaming
        """
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        OLD CODE IF NOT WORKING WITH UPDATE FIX OR UNCOMMENT
        ALSO CHANGE profile.set_... to color_sensor.set_...
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        """

        profile = self.pipeline.start(config)

        color_sensor = profile.get_device().query_sensors()[1]
        color_sensor.set_option(rs.option.enable_auto_exposure, False)
        color_sensor.set_option(rs.option.enable_auto_white_balance, False)
        color_sensor.set_option(rs.option.white_balance, 3300)
        color_sensor.set_option(rs.option.exposure, 80)

        align_to = rs.stream.color
        self.align = rs.align(align_to)

    def getDepth(self, x, y):
        return self.depth_image.get_distance(x, y)

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

        # Align the depth frame to color frame
        aligned_frames = self.align.process(frames)

        # Get aligned frames
        aligned_depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()

        # Validate that both frames are valid
        if not aligned_depth_frame or not color_frame:
            print("Depth and color frames are not valid")
            return None

        self.depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        return color_image