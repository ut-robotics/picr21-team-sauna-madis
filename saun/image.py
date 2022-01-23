#from tkinter import S
import pyrealsense2 as rs
import numpy as np
import cv2

class Image:
    #Data
    aligned_depth_frame = 0
    depth = 0
    pipeline = None

    def __init__(self):
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

    def get_rbg_image(self):
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
        self.frames = self.pipeline.wait_for_frames()
        # frames.get_depth_frame() is a 640x360 depth image

        # Align the depth frame to color frame
        self.aligned_frames = self.align.process(self.frames)

        # Get aligned frames
        self.aligned_depth_frame = self.aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
        self.color_frame = self.aligned_frames.get_color_frame()

        # Validate that both frames are valid
        if not self.aligned_depth_frame or not self.color_frame:
            print("Dept and color frames are not valid")
            return None

        depth_image = np.asanyarray(self.aligned_depth_frame.get_data())
        color_image = np.asanyarray(self.color_frame.get_data())

        # Remove background - Set pixels further than clipping_distance to grey
        grey_color = 153
        depth_image_3d = np.dstack((depth_image,depth_image,depth_image)) #depth image is 1 channel, color is 3 channels
        bg_removed = np.where((depth_image_3d > self.clipping_distance) | (depth_image_3d <= 0), grey_color, color_image)

        # Render images:
        #   depth align to color on left
        #   depth on right
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        images = np.hstack((bg_removed, depth_colormap))

        return color_image