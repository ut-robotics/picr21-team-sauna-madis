from enum import Enum

class MoveStyle(Enum):
    CONTROLLER = 1
    AUTO = 2

class ActiveState(Enum):
    FINDBALL = 1
    MOVE2BALL = 2
    FINDBASKET = 3
    ALIGNBASKET = 4

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
    OBJECT = "blue" #None

class BallHL(Enum):
    lH = 18
    lS = 86
    lV = 43
    hH = 81
    hS = 184
    hV = 117

class BlueBasketHL(Enum):
    lH = 93
    lS = 133
    lV = 75
    hH = 112
    hS = 202
    hV = 97

class PinkBasketHL(Enum):
    lH = 170
    lS = 183
    lV = 187
    hH = 178
    hS = 255
    hV = 255
