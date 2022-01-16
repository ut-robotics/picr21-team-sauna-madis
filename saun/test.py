from image import *
from imageProcess import *

pilt = image()
pilditootlusPall = imageProcess(50, 9999999, "ball")
pilditootlusKorv = imageProcess(50, 9999999, "blue")
while True:
    pilditootlusPall.find_objects(pilt.get_rbg_image())
    cords = pilditootlusPall.getcords()
    print(str(cords) + "ball")
    cords = pilditootlusKorv.getcords(pilt.get_rbg_image())
    print(str(cords) + "blue")