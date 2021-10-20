#!/usr/bin/env python3

import movement
import keyboard

while(True):
    if keyboard.is_pressed("q"):
        print("Stopped by keypress")
        movement.stop()
        break