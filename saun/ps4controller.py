import movement
from pyPS4Controller.controller import Controller
from threading import Thread
from saun.movement import Movement
from var import *

class MyController(Controller):
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        self.movement = movement.Movement()
        self.movement_style = MoveStyle.AUTO

    def get_movement_style(self):
        return self.movement_style

    def on_x_press(self):
        if self.movement_style == MoveStyle.AUTO:
            self.movement_style = MoveStyle.CONTROLLER
        else:
            self.movement.set_movestyle(MoveStyle.AUTO)

    def on_left_arrow_press(self):

        self.movement.set_movement(180, 30, 0, 0)

    def on_right_arrow_press(self):
        self.movement.set_movement(0, 30, 0, 0)

    def on_left_right_arrow_release(self):
        self.movement.stop()

    def on_square_press(self):
        self.throwerspeed = self.throwerspeed - 100
        print(self.throwerspeed)

    def on_triangle_press(self):
        self.throwerspeed = self.throwerspeed + 100
        print(self.throwerspeed)

    def on_up_arrow_press(self):
        self.movement.set_movement(90, 40, 0, 0)

        # self.throwerspeed = self.throwerspeed+100
        # print(self.throwerspeed)

    def on_down_arrow_press(self):
        self.movement.set_movement(270, 40, 0, 0)

        # self.throwerspeed = self.throwerspeed-100
        # print(self.throwerspeed)

    def on_circle_press(self):
        self.movement.thrower(self.throwerspeed)

    def on_R1_press(self):
        self.movement.set_movement(0, 0, -20, 0)
        # self.movement.set_movement(90,40,0,0)#direction, robotspeed, rotspeed, throwerSpeed

    def on_R1_release(self):
        print("STOP")
        self.movement.stop()

    def on_L1_press(self):
        self.movement.set_movement(0, 0, 20, 0)
        # self.movement.set_movement(270,40,0,0)

    def on_L1_release(self):
        self.movement.stop()

class controller:

    def __init__(self):
        self.stopped = False
        self.throwerspeed = 200
        self.movement_style = MoveStyle.AUTO

    def start(self):
        Thread(target=self.listen, args=()).start()
        return self

    def listen(self):
        controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
        controller.listen(timeout=60)
        controller.get_movement_style()

    def get_movement_style(self):
        return self.movement_style






