#!/usr/bin/env python3

import math
import /home/sauna/.local/lib/python3.8/site-packages/serial

firstAngle = 0
secondAngle = 120
thirdAgnle = 240

ser = serial.Serial(port="/dev/ttyACM0",
           baudrate=115200,
           timeout = 2)

def omniWheel(speed, angle, direction):
    vel = speed * math.cos(math.radians(direction - angle))

    return vel

def setMovement(direction):
    print("Moving")
    speed = 50
    x = int(omniWheel(speed, firstAngle, direction))
    y = int(omniWheel(speed, secondAngle, direction))
    z = int(omniWheel(speed, thirdAgnle, direction))
    text = ("<hhhHH",str(x), str(y), str(y), "0xAAAA")

    ser.write(text.encode("utf-8"))

def stop():
    print("STOP")
    ser.write("<hhhHH,0,0,0,0xAAAA".encode("utf-8"))