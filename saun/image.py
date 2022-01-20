import pyrealsense2 as rs
import numpy as np
import cv2

class Image:
    #Data
    depth_frame = 0
    depth = 0
    pipeline = 0

    def __init__(self):
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

        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 60)
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 60)

        try:
            self.pipeline.stop()
        except:
            print("camera oli juba stopped")

        # Start streaming
        color_sensor = self.pipeline.start(config).get_device().query_sensors()[1]
        color_sensor.set_option(rs.option.enable_auto_exposure, False)
        color_sensor.set_option(rs.option.enable_auto_white_balance, False)

        color_sensor.set_option(rs.option.white_balance, 3300)
        color_sensor.set_option(rs.option.exposure, 80)

    def getDepth(self, x, y):
        self.depth = self.depth_frame.get_distance(x, y)
        return self.depth

    def get_rbg_image(self):
        
        frames = self.pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        self.depth_frame = frames.get_depth_frame()
        color_image = np.asanyarray(color_frame.get_data())
        hsv = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)

        return hsv