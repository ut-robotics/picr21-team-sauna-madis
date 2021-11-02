#!/usr/bin/env python3

import math
import serial
import struct

firstAngle = 40
secondAngle = 140
thirdAgnle = 270

#kiirused 0-32767   65500-32768

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
    print("X: " + str(x))
    y = int(omniWheel(speed, secondAngle, direction))
    print("Y: " + str(y))
    z = int(omniWheel(speed, thirdAgnle, direction))
    print("Z: " + str(z))
    package = struct.pack("<hhhHH", x, y, z, 0, 0xAAAA)

    ser.write(package)

def throwBall():
    ser.write(struct.pack("<hhhHH", 10001, 10000, 0, 200, 0xAAAA))

def spinAroundBall():
    return 0

def turnLeft():
    return 0

def turnRight():
    return 0

def spinRight():
    ser.write(struct.pack("<hhhHH", 10001, 10000, 10000, 0, 0xAAAA))

def forward():
    ser.write(struct.pack("<hhhHH", 0, 5000, 60000, 0, 0xAAAA))




def stop():
    print("STOP")
    ser.write(struct.pack("<hhhHH", 0,0,0,0, 0xAAAA))