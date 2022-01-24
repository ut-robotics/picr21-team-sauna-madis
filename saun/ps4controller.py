import movement
from pyPS4Controller.controller import Controller
from threading import Thread
from var import *


#gamestate = "controller" #"auto", "controller"
#gamestate = MoveStyle.AUTO



class controller:
    def __init__(self):
        self.stopped = False
        self.throwerspeed = 200
        self.gamestate= MoveStyle.AUTO

    def start(self):
        Thread(target=self.listen, args=()).start()
        return self
    

    def listen(self):

        class MyController(Controller):

            def __init__(self,gamestate, **kwargs):
                Controller.__init__(self, **kwargs)  

            def on_x_press(self):
                print(self.gamestate)
                if self.gamestate == MoveStyle.AUTO:
                    self.gamestate = MoveStyle.CONTROLLER
                else:
                    self.gamestate = MoveStyle.AUTO
                
            def on_left_arrow_press(self):
                
                self.movement.setMovement(0,0,20,0)

            def on_right_arrow_press(self):
                self.movement.setMovement(0,0,-20,0)

            def on_left_right_arrow_release(self):
                self.movement.stop()

            def on_up_arrow_press(self):
                
                self.throwerspeed = self.throwerspeed+100
                print(self.throwerspeed)

            def on_down_arrow_press(self):
                
                self.throwerspeed = self.throwerspeed-100
                print(self.throwerspeed)

            def on_circle_press(self):
                self.movement.thrower(self.throwerspeed)

            def on_R1_press(self):
                self.movement.setMovement(90,40,0,0)#direction, robotspeed, rotspeed, throwerSpeed

            def on_R1_release(self):
                self.movement.stop()
            
            def on_L1_press(self):
                self.movement.setMovement(270,40,0,0)

            def on_L1_release(self):
                self.movement.stop()

        controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False, gamestate=MoveStyle.AUTO)
        # you can start listening before controller is paired, as long as you pair it within the timeout window
        controller.listen(timeout=60)





