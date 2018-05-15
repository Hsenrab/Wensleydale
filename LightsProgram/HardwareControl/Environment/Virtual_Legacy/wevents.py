import threading
import enum
import time
import random
#from msvcrt import getwch

print("VIRTUAL EVENTS")

# Enum holding the different colour options.
class WColour(enum.Enum):
    Red = 0
    Green = 1
    Blue = 2
    Cyan = 3
    Pink = 4
    Yellow = 5
    White = 6
    MAX = 7

# RBG
colourDi = {}
colourDi[WColour.Red] = (1.0, 0.0, 0.0)
colourDi[WColour.Green] = (0.0, 0.0, 1.0)
colourDi[WColour.Blue] = (0.0, 1.0, 0.0)
colourDi[WColour.Cyan] = (0.0, 0.8, 1.0)
colourDi[WColour.Yellow] = (1.0, 0.0, 0.8)
colourDi[WColour.Pink] = (1.0, 1.0, 0.0)
colourDi[WColour.White] = (1.0, 0.8, 1.0)


# Enum holding the different speed options.
class WSpeed(enum.Enum):
    Sloth = 0
    Tortoise = 1
    Hare = 2
    Cheetah = 3
    MAX = 4

# Number of steps per
speedDi = {}
speedDi[WSpeed.Sloth] = 6
speedDi[WSpeed.Tortoise] = 3
speedDi[WSpeed.Hare] = 2
speedDi[WSpeed.Cheetah] = 1


# Enum holding the different pattern options.
class WPattern(enum.Enum):
    Flashing = 0
    Snakes = 1
    Singles = 2
    Rainbow = 3
    MAX = 4


# Enum holding the different pattern options.
class WBrightness(enum.Enum):
    Low = 0
    Medium = 1
    High = 2
    MAX = 3


brightnessDi = {}
brightnessDi[WBrightness.Low] = 50
brightnessDi[WBrightness.Medium] = 75
brightnessDi[WBrightness.High] = 100


wlight_colour = WColour.Blue
wlight_speed = WSpeed.Hare
wlight_pattern = WPattern.Rainbow
wlight_brightness = WBrightness.Medium


#import termios
#import sys
#import tty
# Raspberry Pi

#def getkey():
 #   fd = sys.stdin.fileno()
 #   old = termios.tcgetattr(fd)
 #   tty.setraw(sys.stdin.fileno())

 #   ch = sys.stdin.read(1)
 #   termios.tcsetattr(fd, termios.TCSADRAIN, old)
 #   return ch


# Windows
#def getkey():
#    return getwch()


def thread1():
    global wlight_colour
    global wlight_speed
    global wlight_pattern
    global wlight_brightness

    lock = threading.Lock()
    
    continue_thread = True
    while continue_thread:
        key = "NULL" #getkey()

        if key == "c":
            with lock:
                new_colour_int = (wlight_colour.value + 1) % WColour.MAX.value
                wlight_colour = WColour(new_colour_int)

        elif key == "s":
            with lock:
                new_speed_int = (wlight_speed.value + 1) % WSpeed.MAX.value
                wlight_speed = WSpeed(new_speed_int)

        elif key == "p":
            with lock:
                new_pattern_int = (wlight_pattern.value + 1) % WPattern.MAX.value
                wlight_pattern = WPattern(new_pattern_int)

        elif key == "b":
            with lock:
                new_brightness_int = (wlight_colour.value + 1) % WBrightness.MAX.value
                wlight_brightness = WBrightness(new_brightness_int)

        elif key == "e":
            raise KeyboardInterrupt



        key = "NULL"

        rand = random.randint(0, 3)
        if rand == 0:
           with lock:
               new_colour_int = (wlight_colour.value + 1) % WColour.MAX.value
               wlight_colour = WColour(new_colour_int)

        elif rand == 1:
           with lock:
               new_speed_int = (wlight_speed.value + 1) % WSpeed.MAX.value
               wlight_speed = WSpeed(new_speed_int)
               
        elif rand == 2:
           with lock:
               new_pattern_int = (wlight_pattern.value + 1) % WPattern.MAX.value
               wlight_pattern = WPattern(new_pattern_int)
               
        time.sleep(10)
        
    exit()

input_thread = threading.Thread(target=thread1).start()

