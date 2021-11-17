import keyboard
import movement

while True:
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
        print("vale nupp")