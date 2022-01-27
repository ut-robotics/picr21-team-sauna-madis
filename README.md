# picr21-team-sauna-madis
##Project in Competitive Robotics 2021

###Required libraries.
ps4controller - Connecting to ps4 controller
pyrealsense2 - Connecting to the camera
threading - Running multiple classes at the same time
opencv-python - Image processing.
time - Mainly for calculating fps
enum - Holding variables
struct - Data package for motors
serial - Communicating with the mainboard
math - For mor complex math operations
numpy - For holding and processing image data

###Required hardware.
Intel realsense2 camera with depth sensor
NUC or similar with preferrably debian based OPSYS
optional - ps4 controller

###Running
Optional-Connect your ps4 controller to your machine.
Run main.py. It starts main thread and waits for controller to connect, if no controller is present, then it only runs on autopilot.

####Controller keybinds
D-pad for driving on all 4 axis. Triggers for turning. X-for chaning autopilot to controller movement only. O-for thrower.





