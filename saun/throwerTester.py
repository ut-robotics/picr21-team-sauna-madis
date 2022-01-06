import cameraImage
import movement
import keyboard
from pyPS4Controller.controller import Controller
from threading import Thread

##              INFO            ##
# X to save
# [] to stop thrower motor
# O to start thrower speed
# Left & Right arrows to set speed steps
# UP & Down arrows to set speed
##################################

distance = 0
throwerspeed = 0
steps = 10

def save():
    with open("throwerData.txt", "a") as file:
        file.write(str(throwerspeed) + ";" + str(distance*100) + "\n")

class controller:

    def __init__(self):
        self.stopped = False

    def start(self):
        Thread(target=self.listen, args=()).start()
        return self

    def listen(self):

        class MyController(Controller):

            def __init__(self, **kwargs):
                Controller.__init__(self, **kwargs)

            def on_x_press(self):
                save()

            def on_circle_press(self):
                global throwerspeed
                movement.thrower(throwerspeed)

            def on_square_press(self):
                movement.stop()

            def on_up_arrow_press(self):
                global throwerspeed, steps
                throwerspeed = throwerspeed + steps
                print(throwerspeed)

            def on_down_arrow_press(self):
                global throwerspeed, steps
                throwerspeed = throwerspeed - steps
                print(throwerspeed)

            def on_left_arrow_press(self):
                global steps
                if (steps > 1):
                    steps = steps / 10

            def on_right_arrow_press(self):
                global steps
                if(steps < 100):
                    steps = steps * 10


        controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
        controller.listen(timeout=60)
cntrl = controller()
cntrl.start()

while True:
    cameraImage.get_image("Blue")
    distance = cameraImage.getDepth(320, 100)
    print("Steps: " + str(steps) + ";  Speed: " + str(throwerspeed) + ";  Distance: " + str(distance))

    if keyboard.is_pressed("q"):
        movement.stop()
        print("Stopped by keypress")
        break


