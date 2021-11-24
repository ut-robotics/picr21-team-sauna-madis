#!/usr/bin/env python3

import math
import serial
import struct
import time

wheelSpeed = 18.75 * 64 / (2 * math.pi * 0.035 * 60)

firstAngle = 0
secondAngle = 130
thirdAgnle = 230

#kiirused 0-32767   65500-32768

ser = serial.Serial(port="/dev/ttyACM0",
           baudrate=115200,
           timeout = 2)

def omniWheel(speed, angle, direction):
    vel = speed * math.cos(math.radians(direction - angle))

    return vel

def setMovement(xSpeed, ySpeed, rotSpeed):
    print("Moving")
    robotSpeed = math.sqrt(xSpeed**2 + ySpeed**2)
    robotDirectionalAngle = math.atan2(xSpeed, ySpeed)

    x = int(omniWheel(robotSpeed, firstAngle, robotDirectionalAngle) + rotSpeed)
    print("X: " + str(x))
    y = int(omniWheel(robotSpeed, secondAngle, robotDirectionalAngle) + rotSpeed)
    print("Y: " + str(y))
    z = int(omniWheel(robotSpeed, thirdAgnle, robotDirectionalAngle) + rotSpeed)
    print("Z: " + str(z))
    package = struct.pack("<hhhHH", x, z, y, 0, 0xAAAA)

    ser.write(package)

def throwBall(speed):
    # tagumine, parem, vasak
    ser.write(struct.pack("<hhhHH", 0, -10, 10, speed, 0xAAAA))
    time.sleep(2)

def spinAroundBall():
    ser.write(struct.pack("<hhhHH", 10, 0, 0, 0, 0xAAAA))

def turnLeft():
    ser.write(struct.pack("<hhhHH", 5, 5, 5, 0, 0xAAAA))

def turnRight():
    ser.write(struct.pack("<hhhHH", -5, -5, -5, 0, 0xAAAA))

def spinRight():
    ser.write(struct.pack("<hhhHH", -5, -5, -5, 0, 0xAAAA))

def forward():
    ser.write(struct.pack("<hhhHH", 0, -20, 20, 0, 0xAAAA))

def forwardspeed(speed, pid):
    
    ser.write(struct.pack("<hhhHH", 0, -speed+pid, speed-pid, 0, 0xAAAA))

def stop():
    print("STOP")
    ser.write(struct.pack("<hhhHH", 0,0,0,0, 0xAAAA))