# Enums and colour/pattern settings.
import enum

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
colourDi = {}
colourDi[WColour.Red] = (1.0, 0.0, 0.0)
colourDi[WColour.Green] = (0.0, 0.0, 1.0)
colourDi[WColour.Blue] = (0.0, 1.0, 0.0)
colourDi[WColour.Cyan] = (0.0, 0.8, 1.0)
colourDi[WColour.Yellow] = (1.0, 0.0, 0.5)
colourDi[WColour.Pink] = (1.0, 0.8, 0.0)
colourDi[WColour.White] = (1.0, 0.5, 0.8)
colourDi[WColour.Orange] = (1.0, 0.0, 0.1)


# Enum holding the different speed options.
class WSpeed(enum.Enum):
    Sloth = 0
    Hare = 1
    Cheetah = 2
    MAX = 3

# Number of steps per
speedDi = {}
speedDi[WSpeed.Sloth] = 6
speedDi[WSpeed.Hare] = 3
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
    MAX = 15 


# Enum holding the direction options.
class WDirection(enum.Enum):
    Forwards = 0
    Backwards = 1
    MAX = 2


