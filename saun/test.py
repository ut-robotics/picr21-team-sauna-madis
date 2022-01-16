from image import *
from imageProcess import *

pilt = image()
pilditootlus = imageProcess(50, 9999999, "ball")
while True:
    pilt = pilt.get_rbg_image()
    objectid = pilditootlus.find_objects(pilt)