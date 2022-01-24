from enum import Enum

class MoveStyle(Enum):
    CONTROLLER = 1
    AUTO = 2

class ActiveState(Enum):
    FINDBALL = 1
    MOVE2BALL = 2
    FINDBASKET = 3
    ALIGNBASKET = 4

