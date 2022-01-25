#!/usr/bin/env python3

# VNC
# 172.17.54.164:5901  172.17.154.183
# madis or password


import movement
from image import *
from imageProcess import *
from var import *
from ps4controller import controller

#Enums
#ImageProcessBasket.OBJECT = BasketColor.BLUE.value
move_style = MoveStyle.AUTO
active_state = ActiveState.FINDBALL


print("Staring controller thread")
cntrl = controller()
cntrl.start()

print(cntrl.movement_style)

# Movement, Image & Image Processing
#   Movement
movement = movement.Movement()

#basket color, will change with ref commands in the future

basket_color = BasketColor.BLUE
#   Image and its processing
image = Image()
proccessed_ball = ImageProcess(ImageProccesBall.MINAREA, ImageProccesBall.MAXAREA, ImageProccesBall.OBJECT)
proccessed_basket = ImageProcess(ImageProcessBasket.MINAREA, ImageProcessBasket.MAXAREA, basket_color)
#Image resolution 848x480@60
camera_x_mid = image.x_resolution/2
# ---------------------------------------------------------------------------Functions

def what_to_do(state, move_style):
        if state == ActiveState.FINDBALL:
            return find_ball(move_style)
        elif state == ActiveState.MOVE2BALL:
            return move_to_ball(move_style)
        elif state == ActiveState.FINDBASKET:
            return find_basket(move_style)
        elif state == ActiveState.ALIGNBASKET:
            return align_basket(move_style)
        elif state == ActiveState.THROWBALL:
            return throw_ball(move_style)

def get_ball_cord(frame):
    proccessed_ball.find_objects(frame, None)
    return proccessed_ball.get_cords()


def get_basket_cord(frame):
    proccessed_basket.find_objects(frame, None)
    return proccessed_basket.get_cords()


# def get_ballNbasket_cord():
#     frame = image.get_aligned_Frames()
#     proccessed_ball.find_objects(frame, None)
#     proccessed_basket.find_objects(frame, None)
#     return proccessed_ball.get_cords(), proccessed_basket.get_cords()


def move_style_check(move_style):
    move_style_new = movement.get_movestyle()

    if move_style == MoveStyle.CONTROLLER and move_style_new == MoveStyle.AUTO:
        print("Changing gamestyle to auto")
        movement.stop()
        move_style = move_style_new
        return move_style

    elif move_style == MoveStyle.AUTO and move_style_new == MoveStyle.CONTROLLER:
        print("Changing gamestyle to controller")
        movement.stop()
        move_style = move_style_new
        return move_style
    else:
        return move_style


def controller_movement(move_style):
    get_ball_cord(image.get_aligned_Frames())
    return move_style_check(move_style)


def find_ball(move_style):
    print("Searching for ball!---------------------------------------------------------")
    movement.set_movement(0, 10, 10, 0)  # direction, robotspeed, rotspeed, throwerspeed
    ball_coordinates = [[0, 0]]

    while ball_coordinates[0][0] == 0:
        if move_style_check(move_style) != move_style: return ActiveState.FINDBALL, move_style.CONTROLLER
        ball_coordinates = get_ball_cord(image.get_aligned_Frames())

    print("Ball found!")
    return ActiveState.MOVE2BALL, move_style


def move_to_ball(move_style):
    print("Moving towards ball---------------------------------------------------------")
    ball_coordinates = get_ball_cord(image.get_aligned_Frames())

    while ball_coordinates[0][0] != 0:  # 848-480
        if move_style_check(move_style) != move_style: return ActiveState.FINDBALL, move_style.CONTROLLER
        ball_coordinates = get_ball_cord(image.get_aligned_Frames())

        movement.set_movement(90, 48 - int(ball_coordinates[0][1] / 10), int((camera_x_mid - ball_coordinates[0][0]) / 10), 0)  # direction, robotspeed, rotspeed, throwerspeed

        if ball_coordinates[0][1] > 400:
            return ActiveState.FINDBASKET, move_style

    return ActiveState.FINDBALL, move_style


def find_basket(move_style):
    print("Searching for basket---------------------------------------------------------")
    ball_coordinates = get_ball_cord(image.get_aligned_Frames())

    while ball_coordinates[0][0] != 0:
        if move_style_check(move_style) != move_style: return ActiveState.FINDBALL, move_style.CONTROLLER

        x_rotation = (ball_coordinates[0][0] - camera_x_mid) / -20  # -4
        y_rotation = (500 - ball_coordinates[0][1]) / 15

        movement.set_movement(0, 10, int(x_rotation + y_rotation), 0)

        frame = image.get_aligned_Frames()
        ball_coordinates =get_ball_cord(frame)
        basket_coordinates = get_basket_cord(frame)

        print("basket coordinates:" + str(basket_coordinates))

        if basket_coordinates[0][0] != 0:
            return ActiveState.ALIGNBASKET, move_style

    return ActiveState.FINDBALL, move_style

def align_basket(move_style):
    print("Found basket moving to align ---------------------------------------------------------")
    frame = image.get_aligned_Frames()
    ball_coordinates =get_ball_cord(frame)
    basket_coordinates = get_basket_cord(frame)

    while ball_coordinates[0][0] != 0 and basket_coordinates[0][0] != 0:
        if move_style_check(move_style) != move_style: return ActiveState.FINDBALL, move_style.CONTROLLER

        frame = image.get_aligned_Frames()
        ball_coordinates =get_ball_cord(frame)
        basket_coordinates = get_basket_cord(frame)

        x_rotation = (ball_coordinates[0][0] - camera_x_mid) / -8  # -4
        y_rotation = (500 - ball_coordinates[0][1]) / 10

        print("Ball: " + str(ball_coordinates) + " Basket: " + str(basket_coordinates))
        print("X: " + str(x_rotation) + " Y: " + str(y_rotation))

        if basket_coordinates[0][0] < camera_x_mid+80 and basket_coordinates[0][0] > camera_x_mid-60 and ball_coordinates[0][0] < camera_x_mid+70 and ball_coordinates[0][0] > camera_x_mid+30:
            basket_depth = image.getDepth(basket_coordinates[0][0], basket_coordinates[0][1])
            print("Basket distance: " + str(basket_depth))
            if basket_depth > 0.5:
                thrower = int(basket_depth * 100 / 0.3934 + 735)
                movement.set_movement(90, 12, 0, thrower)  # direction, robotspeed, rotspeed, throwerSpeed
                print("Thrower speed: " + str(thrower))
    

                #throw_ball()
                return ActiveState.THROWBALL, move_style


        elif basket_coordinates[0][0] > camera_x_mid:
            movement.set_movement(180, 10, int(x_rotation + y_rotation), 0)
        else:
            movement.set_movement(0, 10, int(x_rotation + y_rotation), 0)

    return ActiveState.FINDBALL, move_style

def throw_ball(move_style):
    print("Throwing ball -------------------------------------------------------------")
    if move_style_check(move_style) != move_style: 
        print("move style check")
        return ActiveState.FINDBALL, move_style.CONTROLLER

    frame = image.get_aligned_Frames()
    ball_coordinates =get_ball_cord(frame)
    basket_coordinates = get_basket_cord(frame)
    x_rotation = (ball_coordinates[0][0] - camera_x_mid) / -20  # -4
    y_rotation = (500 - ball_coordinates[0][1]) / 15

    basket_depth = image.getDepth(basket_coordinates[0][0], basket_coordinates[0][1])
    thrower_speed = int(basket_depth * 100 / 0.3934 + 735)

    if basket_coordinates[0][0] < camera_x_mid+80 and basket_coordinates[0][0] > camera_x_mid-60 and ball_coordinates[0][0] < camera_x_mid+70 and ball_coordinates[0][0] > camera_x_mid+30:
        movement.set_movement(90, 10, 0, thrower_speed)
    elif basket_coordinates[0][0] < camera_x_mid:
        movement.set_movement(70, 10, int(x_rotation + y_rotation), thrower_speed)
    elif basket_coordinates[0][0] > camera_x_mid:
        movement.set_movement(110, 10, int(x_rotation + y_rotation), thrower_speed)
    
    if ball_coordinates[0][1] > 480:
        movement.set_movement(90, 10, 0, thrower_speed)
        time.sleep(1)
        return ActiveState.FINDBALL, move_style
    if ball_coordinates[0][0] == 0:
        print("LOST BALL")
        return ActiveState.FINDBALL, move_style
    return ActiveState.THROWBALL, move_style
# def throw_ball(basket_depth):
#     print("Throwing ball---------------------------------------------------------")
#     # x/0,3934+735
#     movement.set_movement(90, 12, 0, int(basket_depth * 100 / 0.3934 + 735))  # direction, robotspeed, rotspeed, throwerSpeed
#     print("Thrower speed: " + str(basket_depth * 100 / 0.3934 + 735))
#     time.sleep(2)  # for testing purposes


# -------------------------------------------------------------------------------- Main

while True:
    while move_style == MoveStyle.CONTROLLER:
        move_style = controller_movement(move_style)
    while move_style == MoveStyle.AUTO:
        print(active_state)
        active_state, move_style = what_to_do(active_state, move_style)