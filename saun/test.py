from image import *
from imageProcess import *

pilt = image()
pilditootlusPall = imageProcess(50, 9999999, "ball")
pilditootlusKorv = imageProcess(50, 9999999, "blue")
while True:
    omg = pilt.get_rbg_image()
    pall = pilditootlusPall.find_objects(omg)
    cords = pilditootlusPall.getcords()
    print(str(cords) + "ball")
    korv = pilditootlusKorv.find_objects(omg)
    cords = pilditootlusKorv.getcords()
    print(str(cords) + "blue")