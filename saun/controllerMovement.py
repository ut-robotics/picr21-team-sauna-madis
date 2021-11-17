import keyboard
import movement

while True:
    try:
        if keyboard.is_pressed("w"):
            movement.forward()
        elif keyboard.is_pressed("s"):
            movement.stop()
        elif keyboard.is_pressed("a"):
            movement.turnLeft()
        elif keyboard.is_pressed("d"):
            movement.turnRight()
    except:
        print("vale nupp")