import movement
import keyboard
#direction, robotspeed, rotspeed
movement.setMovement(0, 10, 0, 0)

if keyboard.is_pressed("q"):
    movement.stop()
    print("Stopped by keypress")
