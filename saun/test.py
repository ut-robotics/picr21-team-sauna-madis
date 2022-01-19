from image import *
from imageProcess import *

pilt = image()
pilditootlusPall = imageProcess(50, 9999999, "ball")

while True:
    pilditootlusPall.find_objects(pilt.get_rbg_image())
    cords = pilditootlusPall.getcords()
    print(str(cords) + "ball")