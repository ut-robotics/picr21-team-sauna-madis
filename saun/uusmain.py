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

    #cameraImage.get_image("ball")
    
    if move_style_check():
        return True


#def get_coordinates(item):
    # "ball", "basket"
    #cameraImage.get_image(item)
    #coordinates = cameraImage.getCords() # get list [x, y]
    #print("PALLIDE COORDINAADID ON: " + str(coordinates))
    #return coordinates

def find_ball():
    print("Searching for ball!")    
    movement.setMovement(0,10,10,0 ) # direction, robotspeed, rotspeed, throwerspeed
    ball_coordinates = [[0,0]]
    while ball_coordinates[0][0] == 0:
        if move_style_check(): return True
        
        #frame = image.get_rbg_image()
        proccessed_ball.find_objects(image.get_rbg_image())
        ball_coordinates = proccessed_ball.getcords()

        #ball_coordinates = get_coordinates("ball")
    print("Ball found!")
    return False

def move_to_ball():
    
    print("Moving towards ball")
    proccessed_ball.find_objects(image.get_rbg_image())
    ball_coordinates = proccessed_ball.getcords()
    #ball_coordinates = get_coordinates("ball")
    while ball_coordinates[0][0] != 0: #640-480
        if move_style_check(): return True

        proccessed_ball.find_objects(image.get_rbg_image())
        ball_coordinates = proccessed_ball.getcords()

        print(ball_coordinates)
        #ball_coordinates = get_coordinates("ball")
        movement.setMovement(90, 48-int(ball_coordinates[0][1]/10),int((320- ball_coordinates[0][0])/10), 0 )  # direction, robotspeed, rotspeed, throwerspeed
        
        if ball_coordinates[0][1] > 400:
            return False
    return True
    #find_ball()

def find_basket():
    
    global basket_color
    print("Searching for basket")
    
    proccessed_ball.find_objects(image.get_rbg_image())
    ball_coordinates = proccessed_ball.getcords()
    
    #ball_coordinates = get_coordinates("ball")
    while ball_coordinates[0][0] != 0:
        if move_style_check(): return True
        
        #ball_y = 420
#230, 360
        
        x_rotation = (ball_coordinates[0][0]-camera_x_mid)/-20 #-4
        y_rotation = (500-ball_coordinates[0][1])/20

        print(ball_coordinates[0][0])
        print(ball_coordinates[0][1])
        print("X-ROTATION: " + str(int(x_rotation)))
        print("Y-ROTATION: " + str(int(y_rotation)))
        movement.setMovement(0, 10 , int(x_rotation+y_rotation), 0) #ball_coordinates[0]-camera_x_mid
        
        proccessed_ball.find_objects(image.get_rbg_image())
        ball_coordinates = proccessed_ball.getcords()
        
        #ball_coordinates = get_coordinates("ball")


        proccessed_basket.find_objects(image.get_rbg_image())
        basket_coordinates = proccessed_basket.getcords()
        #basket_coordinates = get_coordinates(basket_color)

        
        if basket_coordinates[0][0] > 310 and basket_coordinates[0][0] < 330:

            
            basket_depth = image.getDepth(basket_coordinates[0][0], basket_coordinates[0][1])

            #basket_depth = cameraImage.getDepth(basket_coordinates[0],basket_coordinates[1]  ) # is the spot right?
            print("Basket distance: " + str(basket_depth))
            if basket_depth > 0.5:
                throw_ball(basket_depth)

def throw_ball(basket_depth):
    print("Throwing ball---------------------------------------------------------")
    # x/0,3934+735
    movement.setMovement(90, 20 , 0 , int(basket_depth*100/0.3934+735) )    #direction, robotspeed, rotspeed, throwerSpeed
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





