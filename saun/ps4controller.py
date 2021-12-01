import movement
from pyPS4Controller.controller import Controller
from threading import Thread

gamestate = "auto" #"auto", "controller"

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

            def on_up_arrow_press(self):
                movement.forward()
            def on_up_down_arrow_release(self):
                movement.stop()




        controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
        # you can start listening before controller is paired, as long as you pair it within the timeout window
        controller.listen(timeout=60)
    
    def getKey(self):
        
        return (self.key)





