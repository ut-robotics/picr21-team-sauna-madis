import movement
import keyboard

while True:

    movement.setMovement(0,50,10)

    if keyboard.is_pressed("q"):
        movement.stop()
        print("Stopped by keypress")
        break