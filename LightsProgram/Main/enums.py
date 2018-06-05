# Enums and colour/pattern settings.
import enum
import numpy as np

# Enum holding the different colour options.
class WColour(enum.Enum):
    Red = 0
    Green = 1
    Blue = 2
    Cyan = 3
    Pink = 4
    Yellow = 5
    White = 6
    Orange = 7
    MAX = 8

# RBG
dimmming_factor = 1
colourDi = {}
colourDi[WColour.Red] = np.array([1.0, 0.0, 0.0])*dimmming_factor
colourDi[WColour.Green] = np.array([0.0, 0.0, 1.0])*dimmming_factor
colourDi[WColour.Blue] = np.array([0.0, 1.0, 0.0])*dimmming_factor
colourDi[WColour.Cyan] = np.array([0.0, 0.6, 0.8])*dimmming_factor
colourDi[WColour.Yellow] = np.array([1.0, 0.0, 0.4])*dimmming_factor
colourDi[WColour.Pink] = np.array([0.8, 0.6, 0.0])*dimmming_factor
colourDi[WColour.White] = np.array([0.7, 0.3, 0.4])*dimmming_factor
colourDi[WColour.Orange] = np.array([1.0, 0.0, 0.1])*dimmming_factor


# Enum holding the different speed options.
class WSpeed(enum.Enum):
    Sloth = 0
    Hare = 1
    Cheetah = 2
    MAX = 3

# Number of steps per
speedDi = {}
speedDi[WSpeed.Sloth] = 1
speedDi[WSpeed.Hare] = 1
speedDi[WSpeed.Cheetah] = 1


# Enum holding the different pattern options.
class WPattern(enum.Enum):
    Flashing = 0
    Snakes = 1
    Singles = 2
    Slide = 3
    BlockedSlide = 4
    RainbowSlide = 5
    Rainbow = 6
    AllOn = 7
    AllOff = 8
    MovingMorse = 9
    FixedMorse = 10
    Twinkle = 11
    RandomInOut = 12
    ColourSnakesCombine = 13
    BiColourSnakesCombine = 14
    EndTest = 15
    MAX = 16


# Enum holding the direction options.
class WDirection(enum.Enum):
    Forwards = 0
    Backwards = 1
    MAX = 2


