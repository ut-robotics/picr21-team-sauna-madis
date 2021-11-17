import keyboard
import movement
from sshkeyboard import listen_keyboard

def press(key):
    if key=="up":
        print("ControllerEdasi")
        movement.forward()
    elif key == "down":
        print("down pressed")
        movement.stop()
    elif key == "left":
        print("left pressed")
        movement.turnLeft()
    elif key == "right":
        movement.turnRight()
        print("right pressed")

listen_keyboard(on_press=press)


""" //while True:
    try:
        if keyboard.is_pressed("w"):
            print("ControllerEdasi")
            movement.forward()
        elif keyboard.is_pressed("s"):
            print("stop")
            movement.stop()
        elif keyboard.is_pressed("a"):
            print("ControllerVasakule")
            movement.turnLeft()
        elif keyboard.is_pressed("d"):
            print("ControllerParemale")
            movement.turnRight()
        
        if keyboard.is_pressed("q"):
            movement.stop()
            print("Stopped by keypress")
            break
    except:
        break
        print("vale nupp") """