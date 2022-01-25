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
active_state = ActiveState.FINDBALL
move_style = MoveStyle.AUTO


print("Staring controller thread")
cntrl = controller()
cntrl.start()


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
camera_x_mid = int(image.x_resolution/2)
print(camera_x_mid)
# ---------------------------------------------------------------------------Functions

def what_to_do(state):
        if state == ActiveState.FINDBALL:
            return find_ball()
        elif state == ActiveState.MOVE2BALL:
            return move_to_ball()
        elif state == ActiveState.FINDBASKET:
            return find_basket()
        elif state == ActiveState.ALIGNBASKET:
            return align_basket()
        elif state == ActiveState.THROWBALL:
            return throw_ball()

def get_ball_cord(frame):
    proccessed_ball.find_objects(frame, None)
    return proccessed_ball.get_cords()


def get_basket_cord(frame):
    proccessed_basket.find_objects(frame, None)
    return proccessed_basket.get_cords()


def move_style_check(move_style):
    move_style_new = cntrl.get_movement_style()

    if move_style != move_style_new:
        print("Changing movestyle")
        movement.stop()
        return move_style_new
    else:
        return move_style


def controller_movement():
    get_ball_cord(image.get_aligned_Frames())


def find_ball():
    print("Searching for ball!---------------------------------------------------------")
    movement.set_movement(0, 10, 10, 0)  # direction, robotspeed, rotspeed, throwerspeed
    ball_coordinates = get_ball_cord(image.get_aligned_Frames())

    if ball_coordinates[0][0] == 0:
        return ActiveState.FINDBALL
    else:
        print("Ball found!")
        return ActiveState.MOVE2BALL


def move_to_ball():
    print("Moving towards ball---------------------------------------------------------")
    ball_coordinates = get_ball_cord(image.get_aligned_Frames())

    if ball_coordinates[0][0] == 0:  # 848-480
        return ActiveState.FINDBALL
    elif ball_coordinates[0][0] != 0:
        print("Have ball")
        movement.set_movement(90, 48 - int(ball_coordinates[0][1] / 10), int((camera_x_mid - ball_coordinates[0][0]) / 10), 0)  # direction, robotspeed, rotspeed, throwerspeed
        if ball_coordinates[0][1] > 400:
            return ActiveState.FINDBASKET
        else:
            return ActiveState.MOVE2BALL
    else:
        print("Not working correctly")
        return ActiveState.FINDBALL



def find_basket():
    print("Searching for basket---------------------------------------------------------")
    frame = image.get_aligned_Frames()
    ball_coordinates = get_ball_cord(frame)

    if ball_coordinates[0][0] == 0:
        return ActiveState.FINDBALL
    elif ball_coordinates[0][0] != 0:
        x_rotation = (ball_coordinates[0][0] - camera_x_mid) / -20  # -4
        y_rotation = (500 - ball_coordinates[0][1]) / 15

        movement.set_movement(0, 10, int(x_rotation + y_rotation), 0)

        basket_coordinates = get_basket_cord(frame)

        if basket_coordinates[0][0] != 0:
            print("basket coordinates:" + str(basket_coordinates))
            return ActiveState.ALIGNBASKET
        else:
            return ActiveState.FINDBASKET
    else:
        print("Not working correctly")
        return ActiveState.FINDBALL

def align_basket():
    print("Found basket moving to align ---------------------------------------------------------")
    frame = image.get_aligned_Frames()
    ball_coordinates = get_ball_cord(frame)
    basket_coordinates = get_basket_cord(frame)

    if ball_coordinates[0][0] == 0 and basket_coordinates[0][0] == 0:
        return ActiveState.FINDBALL
    elif ball_coordinates[0][0] != 0 and basket_coordinates[0][0] != 0:

        x_rotation = (ball_coordinates[0][0] - camera_x_mid) / -8  # -4
        y_rotation = (500 - ball_coordinates[0][1]) / 10

        print("Ball: " + str(ball_coordinates) + " Basket: " + str(basket_coordinates))
        print("X: " + str(x_rotation) + " Y: " + str(y_rotation))

        if basket_coordinates[0][0] < camera_x_mid+80 and basket_coordinates[0][0] > camera_x_mid-60 and ball_coordinates[0][0] < camera_x_mid+70 and ball_coordinates[0][0] > camera_x_mid+30:
            basket_depth = image.getDepth(basket_coordinates[0][0], basket_coordinates[0][1])
            print("Basket distance: " + str(basket_depth))
            if basket_depth > 0.5:

                #throw_ball()
                return ActiveState.THROWBALL

        elif basket_coordinates[0][0] > camera_x_mid:
            movement.set_movement(180, 10, int(x_rotation + y_rotation), 0)
            return ActiveState.ALIGNBASKET
        elif basket_coordinates[0][0] < camera_x_mid:
            movement.set_movement(0, 10, int(x_rotation + y_rotation), 0)
            return ActiveState.ALIGNBASKET
        print("BALL TOO CLOSE")
        return ActiveState.FINDBALL
    else:
        print("Not working correctly")
        return ActiveState.FINDBALL

def throw_ball():
    print("Throwing ball -------------------------------------------------------------")
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
        return ActiveState.FINDBALL
    if ball_coordinates[0][0] == 0:
        print("LOST BALL")
        return ActiveState.FINDBALL
    return ActiveState.THROWBALL
# -------------------------------------------------------------------------------- Main

while True:
    move_style = move_style_check(move_style)
    print("Before statemnts")
    if move_style == MoveStyle.CONTROLLER:
        controller_movement()
    elif active_state == None:
        break
    else:
        active_state = what_to_do(active_state)
