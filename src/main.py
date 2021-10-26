#!/usr/bin/env python3

#VNC
#172.17.54.164:5900
#madis

import movement
import keyboard

while(True):
    movement.spin
    if keyboard.is_pressed("q"):
        print("Stopped by keypress")
        movement.stop()
        break