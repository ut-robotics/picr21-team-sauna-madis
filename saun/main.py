#!/usr/bin/env python3

#VNC
#172.17.54.164:5901  172.17.154.183
#madis or password

from math import pi
from sys import breakpointhook
import movement
#import cameraImage
import time
from image import *
from imageProcess import *
from ps4controller import controller
from ps4controller import getgamestate

camera_x_mid = 320

basket_color = "blue" # "blue" , "pink"
move_style = "auto" # "auto" , "controller"

print("Stardin controlleri threadi")
cntrl = controller()
cntrl.start()

image = image()
proccessed_ball = imageProcess(70,999999, "ball")
proccessed_basket = imageProcess(150,999999, basket_color)


def move_style_check():
    global move_style
    move_style_new = getgamestate()

    if move_style == "controller" and move_style_new == "auto":
        print("Changing gamestyle to auto")
        movement.stop()
        move_style = move_style_new
        return True
         
    elif move_style == "auto" and move_style_new =="controller":
        print("Changing gamestyle to controller")
        movement.stop()
        move_style = move_style_new
        return True

def controller_movement():
    ball_image = image.get_rbg_image()
    proccessed_ball.find_objects(ball_image)

    if move_style_check():
        return True

def find_ball():
    print("Searching for ball!---------------------------------------------------------")
    movement.setMovement(0,10,10,0 ) # direction, robotspeed, rotspeed, throwerspeed
    ball_coordinates = [[0,0]]
    while ball_coordinates[0][0] == 0:
        if move_style_check(): return True

        proccessed_ball.find_objects(image.get_rbg_image())
        ball_coordinates = proccessed_ball.getcords()

    print("Ball found!")
    return False

def move_to_ball():
    
    print("Moving towards ball---------------------------------------------------------")
    proccessed_ball.find_objects(image.get_rbg_image())
    ball_coordinates = proccessed_ball.getcords()

    while ball_coordinates[0][0] != 0: #640-480
        if move_style_check(): return True

        proccessed_ball.find_objects(image.get_rbg_image())
        ball_coordinates = proccessed_ball.getcords()

        movement.setMovement(90, 48-int(ball_coordinates[0][1]/10),int((320- ball_coordinates[0][0])/10), 0 )  # direction, robotspeed, rotspeed, throwerspeed
        
        if ball_coordinates[0][1] > 400:
            return False
    return True

def find_basket():
    
    global basket_color
    print("Searching for basket---------------------------------------------------------")
    someWhereMiddle = False
    proccessed_ball.find_objects(image.get_rbg_image())
    ball_coordinates = proccessed_ball.getcords()

    while ball_coordinates[0][0] != 0:
        if move_style_check(): return True

        x_rotation = (ball_coordinates[0][0]-camera_x_mid)/-20 #-4
        y_rotation = (500-ball_coordinates[0][1])/15

        #print(ball_coordinates[0][0])
        #print(ball_coordinates[0][1])
        #print("X-ROTATION: " + str(int(x_rotation)))
        #print("Y-ROTATION: " + str(int(y_rotation)))
        movement.setMovement(0, 10 , int(x_rotation+y_rotation), 0)
        
        proccessed_ball.find_objects(image.get_rbg_image())
        ball_coordinates = proccessed_ball.getcords()

        proccessed_basket.find_objects(image.get_rbg_image())
        basket_coordinates = proccessed_basket.getcords()
        print("basket coordinates:" + str(basket_coordinates))

        if basket_coordinates[0][0] > 310:
            someWhereMiddle = True
            while someWhereMiddle:
                if basket_coordinates[0][0] > 325 and basket_coordinates[0][0] < 315:
                    someWhereMiddle = False
                    break
                elif basket_coordinates[0][0] > 325:
                    movement.setMovement(180, 10, int(x_rotation+y_rotation), 0)
                else:
                    movement.setMovement(0, 10 , int(x_rotation+y_rotation), 0)

            basket_depth = image.getDepth(basket_coordinates[0][0], basket_coordinates[0][1])

            print("Basket distance: " + str(basket_depth))
            if basket_depth > 0.5:
                throw_ball(basket_depth)

def throw_ball(basket_depth):
    print("Throwing ball---------------------------------------------------------")
    # x/0,3934+735
    movement.setMovement(90, 20 , 0 , int(basket_depth*100/0.3934+735) )  #direction, robotspeed, rotspeed, throwerSpeed
    print("Thrower speed: "+ str(basket_depth*100/0.3934+735))
    time.sleep(2) #for testing purposes

while True:
    print(move_style)
    while move_style== "controller":
        if controller_movement():
            break
    while move_style == "auto":
        if find_ball(): break
        if move_to_ball(): break
        if find_basket(): break





