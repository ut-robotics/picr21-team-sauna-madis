import movement
import keyboard

while True:

    movement.setMovement(90)

    if keyboard.is_pressed("q"):
        movement.stop()
        print("Stopped by keypress")
        break