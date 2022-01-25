import _thread
import json
from var import *

class Client:
    def __init__(self, ws):
        self.stopped = False
        self.signal = False
        self.robot = "SaunaMadis"
        self.basket = BasketColor.BLUE
        self.ws = ws


    def listen(self, ws):
        def run(*args):
            while not self.stopped:
                message = self.ws.recv()
                command = json.loads(message)

                if command["signal"] == "stop" and self.robot in command["targets"]:
                    self.signal = False
                elif command["signal"] == "start" and self.robot in command["targets"]:
                    index = command["targets"].index(self.robot)
                    color = command["baskets"][index]
                    if color == "blue":
                        self.basket = BasketColor.BLUE
                    elif color == "magenta":
                        self.basket = BasketColor.PINK
                    self.signal = True
                else:
                    pass
        _thread.start_new_thread(run, ())

    def getter(self):
        return self.signal, self.basket

    def stop(self):
        self.stopped = True