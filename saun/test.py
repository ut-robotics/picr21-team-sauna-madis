import movement
import keyboard

movement.setMovement(90, 0)

if keyboard.is_pressed("q"):
    movement.stop()
    print("Stopped by keypress")
