from image import *
from imageProcess import *
import movement

pilt = Image()
pilditootlusPall = ImageProcess(50, 9999999, "ball")

while True:
    movement.setMovement(0,5,0,0)
    pilditootlusPall.find_objects(pilt.get_rbg_image())
    cords = pilditootlusPall.getcords()
    print(str(cords) + "ball")