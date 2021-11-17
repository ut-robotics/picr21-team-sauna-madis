#!/usr/bin/env python3

import math
import serial
import struct
import time

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
    # tagumine, parem, vasak
    ser.write(struct.pack("<hhhHH", 0, -50, 50, 200, 0xAAAA))
    time.sleep(2)

def spinAroundBall():
    ser.write(struct.pack("<hhhHH", 10, 0, 0, 0, 0xAAAA))

def turnLeft():
    return 0

def turnRight():
    return 0

def spinRight():
    ser.write(struct.pack("<hhhHH", -5, -5, -5, 0, 0xAAAA))

def forward():
    ser.write(struct.pack("<hhhHH", 0, -50, 50, 0, 0xAAAA))

def forwardspeed(speed, pid):
    
    ser.write(struct.pack("<hhhHH", 0, -speed+pid, speed-pid, 0, 0xAAAA))



def stop():
    print("STOP")
    ser.write(struct.pack("<hhhHH", 0,0,0,0, 0xAAAA))