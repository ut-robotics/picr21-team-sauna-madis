#!/usr/bin/env python3

#VNC
#172.17.54.164:5901  172.17.154.183
#madis or password

from math import pi
import movement
import cameraImage
from saun.movement import throwBall

camera_x_mid = 320

basket_color = "blue" # "blue" , "pink"
move_style = "auto" # "auto" , "controller"




def get_coordinates(item):
    # "ball", "basket"
    cameraImage.get_image(item)
    coordinates = cameraImage.getCords() # get list [x, y]
    return coordinates

def find_ball():
    print("Searching for ball!")    
    movement.setMovement( ) # direction, robotspeed, rotspeed
    ball_coordinates = [0,0]
    while ball_coordinates[0] == 0:
       ball_coordinates = get_coordinates("ball")
    print("Ball found!")

def move_to_ball():
    print("Moving towards ball")
    ball_coordinates = get_coordinates("ball")
    while ball_coordinates[0] != 0: #640-480
        movement.setMovement(90, 48-int(ball_coordinates[1]/10),int((320- ball_coordinates[0])/10), 0 )  # direction, robotspeed, rotspeed
        if ball_coordinates[1] > 600:
            find_basket()
            
    find_ball()

def find_basket():
    print("Searching for basket")
    ball_coordinates = get_coordinates("ball")
    while ball_coordinates[0] != 0:
        ball_coordinates = get_coordinates("ball")
        movement.setMovement(180, 10, ball_coordinates[0]-camera_x_mid, 0)
        basket_coordinates = get_coordinates("basket")

        if basket_coordinates[0] < 300 and basket_coordinates[0] > 340:
            basket_depth = cameraImage.getDepth() # is the spot right?
            
            if basket_depth > 0.5:
                throwBall(basket_depth)

def throw_ball(basket_depth):
    print("Throwing ball")
    movement.setMovement(90, 20 , 0 , basket_depth*200 )    #direction, robotspeed, rotspeed, throwerSpeed

while True:
    find_ball()
    move_to_ball()



