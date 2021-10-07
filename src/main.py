import movement
import keyboard

while(True):
    arv = movement.setMovement(int(input()))
    if keyboard.is_pressed("q"):
        print("Stopped by keypress")
        movement.stop()
        break