import movement
from pyPS4Controller.controller import Controller
from threading import Thread

from saun.movement import throwBall

gamestate = "controller" #"auto", "controller"
throwerspeed = 200

def getgamestate():
    return gamestate

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
                global gamestate

                print("Hello world")
                if gamestate == "auto":
                    gamestate = "controller"
                else:
                    gamestate = "auto"
                    
            
            def on_left_arrow_press(self):
                movement.turnLeft()

            def on_right_arrow_press(self):
                movement.turnRight()

            def on_left_right_arrow_release(self):
                movement.stop()

            def on_up_arrow_press(self):
                global throwerspeed
                throwerspeed = throwerspeed+100
                print(throwerspeed)

            def on_down_arrow_press(self):
                global throwerspeed
                throwerspeed = throwerspeed-100
                print(throwerspeed)

            def on_circle_press(self):
                movement.thrower()

            def on_R1_press(self):
                movement.forward()

            def on_R1_release(self):
                movement.stop()
            
            def on_L1_press(self):
                movement.backward()

            def on_L1_release(self):
                movement.stop()




        controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
        # you can start listening before controller is paired, as long as you pair it within the timeout window
        controller.listen(timeout=60)





