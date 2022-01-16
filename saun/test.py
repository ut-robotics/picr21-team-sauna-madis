import movement
import keyboard
#direction, robotspeed, rotspeed
movement.setMovement(180, 10, -5, 0)

if keyboard.is_pressed("q"):
    movement.stop()
    print("Stopped by keypress")
