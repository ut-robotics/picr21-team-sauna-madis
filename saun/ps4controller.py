from main import kask
from pyPS4Controller.controller import Controller
from threading import Thread

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
                print("Hello world")
                kask()

            def on_x_release(self):
                print("Goodbye world")

        controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
        # you can start listening before controller is paired, as long as you pair it within the timeout window
        controller.listen(timeout=60)





