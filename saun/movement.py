#!/usr/bin/env python3
import math
from shutil import move
import serial
from serial.tools import list_ports
import struct
#from saun.main import move_style_check
from var import *



class Movement:
    move_style = MoveStyle.AUTO
    def __init__(self):
        self.wheelSpeed = 18.75 * 64 / (2 * math.pi * 0.035 * 60)
        self.firstAngle = 0
        self.secondAngle = 130
        self.thirdAgnle = 230

        

        #self.ser = serial.Serial(port="/dev/ttyACM0", baudrate=115200, timeout=2)
        self.ser = serial.Serial(port=self.findPort("206638925056"), baudrate=115200, timeout=2)

    def findPort(self, serialNr):
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if serialNr == p.serial_number:
                return p.device
    
    def getMovestyle(self):
        move_style = Movement.move_style
        return move_style
    
    def setMovestyle(self, style):
        move_style = style
        return move_style

    def setMovement(self, direction ,robotSpeed, rotSpeed, throwerSpeed):
        #print("Moving")
        x = int(self.omniWheel(robotSpeed, self.firstAngle, direction) + rotSpeed)
        #print("X: " + str(x))
        y = int(self.omniWheel(robotSpeed, self.secondAngle, direction) + rotSpeed)
        #print("Y: " + str(y))
        z = int(self.omniWheel(robotSpeed, self.thirdAgnle, direction) + rotSpeed)
        #print("Z: " + str(z))

        package = struct.pack("<hhhHH", x, z, y, throwerSpeed, 0xAAAA)
        self.ser.write(package)

    def thrower(self, speed):
        self.ser.write(struct.pack("<hhhHH", 0, 0, 0, speed, 0xAAAA))

    def omniWheel(self, speed, angle, direction):
        vel = speed * math.cos(math.radians(direction - angle))
        return vel

    def stop(self):
        print("STOP")
        self.ser.write(struct.pack("<hhhHH", 0,0,0,0, 0xAAAA))
