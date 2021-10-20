#!/usr/bin/env python3

import movement
import /home/sauna/.local/lib/python3.8/site-packages/keyboard

while(True):
    if keyboard.is_pressed("q"):
        print("Stopped by keypress")
        movement.stop()
        break