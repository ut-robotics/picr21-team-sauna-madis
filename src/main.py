#!/usr/bin/env python3

#VNC
#172.17.54.164:5900
#madis

import movement
import keyboard
import keyboard

try:
    while True:
        movement.spin(20)
        if keyboard.is_pressed("q"):
            print("Stopped by keypress")
            break
finally:
    movement.stop()