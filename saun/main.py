#!/usr/bin/env python3

# VNC
# 172.17.54.164:5901  172.17.154.183
# madis or password


import movement
from image import *
from imageProcess import *
from var import *
from ps4controller import Sontroller
from ps4controller import getgamestate


#848x480@60
camera_x_mid = 424

basket_color = "blue"  # "blue" , "pink"
# move_style = "auto"  # "auto" , "controller"
move_style = MoveStyle.AUTO

print("Staring controller thread")
cntrl = Sontroller()
cntrl.start()

# Image and its processing
image = Image()
proccessed_ball = ImageProcess(70, 999999, "ball")
proccessed_basket = ImageProcess(150, 999999, basket_color)
window = cv2.namedWindow("SaunaMadis")

# ---------------------------------------------------------------------------Functions
def get_ball_cord():
    proccessed_ball.find_objects(image.get_rbg_image(), window)
    return proccessed_ball.getcords()


def get_basket_cord():
    proccessed_basket.find_objects(image.get_rbg_image(), window)
    return proccessed_basket.getcords()


def get_ballNbasket_cord():
    proccessed_ball.find_objects(image.get_rbg_image(), window)
    proccessed_basket.find_objects(image.get_rbg_image(), window)
    return proccessed_ball.getcords(), proccessed_basket.getcords()


def move_style_check(move_style):
    move_style_new = getgamestate()

    if move_style == MoveStyle.CONTROLLER and move_style_new == MoveStyle.AUTO:
        print("Changing gamestyle to auto")
        movement.stop()
        move_style = move_style_new
        return True

    elif move_style == MoveStyle.AUTO and move_style_new == MoveStyle.CONTROLLER:
        print("Changing gamestyle to controller")
        movement.stop()
        move_style = move_style_new
        return True


def controller_movement():
    get_ball_cord()

    if move_style_check(move_style):
        return True


def find_ball():
    print("Searching for ball!---------------------------------------------------------")
    movement.setMovement(0, 10, 10, 0)  # direction, robotspeed, rotspeed, throwerspeed
    ball_coordinates = [[0, 0]]
    while ball_coordinates[0][0] == 0:
        if move_style_check(move_style): return True

        ball_coordinates = get_ball_cord()

    print("Ball found!")
    return False


def move_to_ball():
    print("Moving towards ball---------------------------------------------------------")
    ball_coordinates = get_ball_cord()

    while ball_coordinates[0][0] != 0:  # 848-480
        if move_style_check(move_style): return True

        ball_coordinates = get_ball_cord()

        movement.setMovement(90, 48 - int(ball_coordinates[0][1] / 10), int((camera_x_mid - ball_coordinates[0][0]) / 10), 0)  # direction, robotspeed, rotspeed, throwerspeed

        if ball_coordinates[0][1] > 400:
            return False
    return True


def find_basket():
    print("Searching for basket---------------------------------------------------------")
    ball_coordinates = get_ball_cord()

    while ball_coordinates[0][0] != 0:
        if move_style_check(move_style): return True

        x_rotation = (ball_coordinates[0][0] - camera_x_mid) / -20  # -4
        y_rotation = (500 - ball_coordinates[0][1]) / 15

        movement.setMovement(0, 10, int(x_rotation + y_rotation), 0)

        ball_coordinates, basket_coordinates = get_ballNbasket_cord()

        print("basket coordinates:" + str(basket_coordinates))

        if basket_coordinates[0][0] != 0:
            return False


def align_basket():
    print("Found basket moving to align ---------------------------------------------------------")
    ball_coordinates, basket_coordinates = get_ballNbasket_cord()
    while ball_coordinates[0][0] != 0 and basket_coordinates[0][0] != 0:
        if move_style_check(move_style): return True

        ball_coordinates, basket_coordinates = get_ballNbasket_cord()
        x_rotation = (ball_coordinates[0][0] - camera_x_mid) / - 33  # -4
        y_rotation = (500 - ball_coordinates[0][1]) / 17
        print("Ball: " + str(ball_coordinates) + " Basket: " + str(basket_coordinates))
        print("X: " + str(x_rotation) + " Y: " + str(y_rotation))
        if basket_coordinates[0][0] < camera_x_mid+5 and basket_coordinates[0][0] > camera_x_mid-5 and ball_coordinates[0][0] < camera_x_mid+5 and ball_coordinates[0][0] > camera_x_mid-5:
            basket_depth = image.getDepth(basket_coordinates[0][0], basket_coordinates[0][1])
            print("Basket distance: " + str(basket_depth))
            if basket_depth > 0.5:
                throw_ball(basket_depth)
                break

        elif basket_coordinates[0][0] > camera_x_mid-5:
            movement.setMovement(180, 7, int(x_rotation - y_rotation), 0)
        else:
            movement.setMovement(0, 7, int(x_rotation + y_rotation), 0)


def throw_ball(basket_depth):
    print("Throwing ball---------------------------------------------------------")
    # x/0,3934+735
    movement.setMovement(90, 20, 0, int(basket_depth * 100 / 0.3934 + 735))  # direction, robotspeed, rotspeed, throwerSpeed
    print("Thrower speed: " + str(basket_depth * 100 / 0.3934 + 735))
    time.sleep(2)  # for testing purposes


# -------------------------------------------------------------------------------- Main

while True:
    print(move_style)
    while move_style == MoveStyle.CONTROLLER:
        if controller_movement():
            break
    while move_style == MoveStyle.AUTO:
        if find_ball(): break
        if move_to_ball(): break
        if find_basket(): break
        if align_basket(): break
