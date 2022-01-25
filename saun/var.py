from enum import Enum

class MoveStyle(Enum):
    CONTROLLER = 1
    AUTO = 2

class ActiveState(Enum):
    FINDBALL = 1
    MOVE2BALL = 2
    FINDBASKET = 3
    ALIGNBASKET = 4
    THROWBALL = 5

class BasketColor(Enum):
    BLUE = "blue"
    PINK = "pink"

# ------------------------------------------------
class ImageProccesBall(Enum):
    MINAREA = 70
    MAXAREA = 999999
    OBJECT = "ball"

class ImageProcessBasket(Enum):
    MINAREA = 150
    MAXAREA = 999999
    OBJECT = "blue" #None, temporary

class BallHL(Enum):
    lH = 65
    lS = 57
    lV = 45
    hH = 83
    hS = 117
    hV = 139

class BlueBasketHL(Enum):
    lH = 40
    lS = 156
    lV = 60
    hH = 115
    hS = 192
    hV = 109

class PinkBasketHL(Enum):
    lH = 170
    lS = 183
    lV = 187
    hH = 178
    hS = 255
    hV = 255
