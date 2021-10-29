#!/usr/bin/env python3

import math
import serial
import struct

firstAngle = 0
secondAngle = 130
thirdAgnle = 260

ser = serial.Serial(port="/dev/ttyACM0",
           baudrate=115200,
           timeout = 2)

def omniWheel(speed, angle, direction):
    vel = speed * math.cos(math.radians(direction - angle))

    return vel

def spinRight():
    ser.write(struct.pack("<hhhHH", 32767, 32767, 32767, 0 0xAAAA))

def setMovement(direction):
    print("Moving")
    speed = 50
    x = int(omniWheel(speed, firstAngle, direction))
    print("X: " + str(x))
    y = int(omniWheel(speed, secondAngle, direction))
    print("Y: " + str(y))
    z = int(omniWheel(speed, thirdAgnle, direction))
    print("Z: " + str(z))
    package = struct.pack("<hhhHH", x, y, z, 0, 0xAAAA)

    ser.write(package)

def stop():
    print("STOP")
    ser.write(struct.pack("<hhhHH", 0,0,0,0, 0xAAAA))