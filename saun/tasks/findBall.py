

from saun import movement
from saun import cameraImage

while True:

    cameraImage.get_image()
    ballX = cameraImage.getCords()

    if ballX[0] != 0:
        print("Leidsin palli")
        if ballX[0] < 300:

            movement.turnRight()

        elif ballX[0] > 340:

            movement.turnLeft()

        else:
            movement.stop()

    movement.spinRight()