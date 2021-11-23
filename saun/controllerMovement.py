import keyboard
import movement
from sshkeyboard import listen_keyboard

def press(key):
    if key=="up":
        print("up pressed")
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

    elif key == 't':
        movement.throwBall(2000)
        print("t pressed")

    elif key == 'o':
        movement.spinAroundBall()
        print("o pressed, spinning around ball")

def main():

    listen_keyboard(on_press=press)

if __name__ =="__main__":
    main()
