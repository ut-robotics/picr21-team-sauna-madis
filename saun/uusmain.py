#!/usr/bin/env python3

#VNC
#172.17.54.164:5901  172.17.154.183
#madis or password

from math import pi
from sys import breakpointhook
import movement
import cameraImage
import time
from ps4controller import controller
from ps4controller import getgamestate

camera_x_mid = 320

basket_color = "blue" # "blue" , "pink"
move_style = "auto" # "auto" , "controller"

print("Stardin controlleri threadi")
cntrl = controller()
cntrl.start()

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
    cameraImage.get_image("ball")
    if move_style_check():
        return True


def get_coordinates(item):
    # "ball", "basket"
    cameraImage.get_image(item)
    coordinates = cameraImage.getCords() # get list [x, y]
    #print("PALLIDE COORDINAADID ON: " + str(coordinates))
    return coordinates

def find_ball():
    print("Searching for ball!")    
    movement.setMovement(0,10,10,0 ) # direction, robotspeed, rotspeed, throwerspeed
    ball_coordinates = [0,0]
    while ball_coordinates[0] == 0:
        if move_style_check(): return True
        ball_coordinates = get_coordinates("ball")
    print("Ball found!")
    return False

def move_to_ball():
    
    print("Moving towards ball")
    ball_coordinates = get_coordinates("ball")
    while ball_coordinates[0] != 0: #640-480
        if move_style_check(): return True
        ball_coordinates = get_coordinates("ball")
        movement.setMovement(90, 48-int(ball_coordinates[1]/10),int((320- ball_coordinates[0])/10), 0 )  # direction, robotspeed, rotspeed, throwerspeed
        
        if ball_coordinates[1] > 350:
            return False
            
    find_ball()

def find_basket():
    
    global basket_color
    print("Searching for basket")
    ball_coordinates = get_coordinates("ball")
    while ball_coordinates[0] != 0:
        if move_style_check(): return True
        ball_coordinates = get_coordinates("ball")
        print(str(int((ball_coordinates[0]-camera_x_mid)/10)))
        movement.setMovement(0, 20, int((ball_coordinates[0]-camera_x_mid)/10), 0) #ball_coordinates[0]-camera_x_mid
        
        basket_coordinates = get_coordinates(basket_color)
        
       # if basket_coordinates[0] < 300 and basket_coordinates[0] > 340:
        #    basket_depth = cameraImage.getDepth(basket_coordinates[0],basket_coordinates[1]  ) # is the spot right?
         #   print("Basket distance: " + str(basket_depth))
          #  if basket_depth > 0.5:
           #     throw_ball(basket_depth)

def throw_ball(basket_depth):
    print("Throwing ball")
    # x/0,3934+735
    movement.setMovement(90, 20 , 0 , basket_depth*100/0.3934+735 )    #direction, robotspeed, rotspeed, throwerSpeed
    print("Thrower speed: "+ str(basket_depth*100/0.3934+735))
    time.sleep(1) #for testing purposes

while True:
    print(move_style)
    while move_style== "controller":
        if controller_movement():
            break
    while move_style == "auto":
        if find_ball(): break
        if move_to_ball(): break
        if find_basket(): break





