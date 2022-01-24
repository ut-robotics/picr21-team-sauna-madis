#!/usr/bin/env python3

import math
import serial
from serial.tools import list_ports
import struct
import time

wheelSpeed = 18.75 * 64 / (2 * math.pi * 0.035 * 60)

firstAngle = 0
secondAngle = 130
thirdAgnle = 230

#kiirused 0-32767   65500-32768
#Asenda port = list_ports.grep(VID:PID)
ser = serial.Serial(port="/dev/ttyACM0", baudrate=115200, timeout = 2)

def omniWheel(speed, angle, direction):
    vel = speed * math.cos(math.radians(direction - angle))
    return vel

def setMovement(direction ,robotSpeed, rotSpeed, throwerSpeed):
    #print("Moving")
    x = int(omniWheel(robotSpeed, firstAngle, direction) + rotSpeed)
    #print("X: " + str(x))
    y = int(omniWheel(robotSpeed, secondAngle, direction) + rotSpeed)
    #print("Y: " + str(y))
    z = int(omniWheel(robotSpeed, thirdAgnle, direction) + rotSpeed)
    #print("Z: " + str(z))

    package = struct.pack("<hhhHH", x, z, y, throwerSpeed, 0xAAAA)
    ser.write(package)

def thrower(speed):
    ser.write(struct.pack("<hhhHH", 0, 0, 0, speed, 0xAAAA))

def stop():
    print("STOP")
    ser.write(struct.pack("<hhhHH", 0,0,0,0, 0xAAAA))