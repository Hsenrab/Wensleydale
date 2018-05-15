import threading
import enum
import time
import random
import RPi.GPIO as GPIO
import Internals.Utils.wlogger as wlogger

import termios
import sys
import tty
#from msvcrt import getwch

print_debug = True

colourInputPin = 7
speedInputPin = 8
patternInputPin = 24


colourOutputPin = 13
speedOutputPin = 16
patternOutputPin = 12


GPIO.setmode(GPIO.BCM)
GPIO.setup(colourInputPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(speedInputPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(patternInputPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(colourOutputPin, GPIO.OUT)
GPIO.setup(speedOutputPin, GPIO.OUT)
GPIO.setup(patternOutputPin, GPIO.OUT)

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
colourDi[WColour.Pink] = (1.0, 1.0, 0.0)
colourDi[WColour.White] = (1.0, 0.8, 1.0)
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
wlight_speed = WSpeed.Cheetah
wlight_pattern = WPattern.Singles
wlight_brightness = WBrightness.Low
button_press_count = 0

#Temp for taking input on keyboard.
def getkey():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    tty.setraw(sys.stdin.fileno())

    ch = sys.stdin.read(1)
    termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch



# This thread listens to the buttons and changes the global variables 
# indicating the colour, speed and pattern. It then stops listening to 
# the given button for a number of cycles so that the buttons can't be 
# spammed.

# Note that the method for doing this is a little odd as it uses the number
# of while cycles do dictate how long a button should be muted rather than
# a unit of time. This is because time.sleep() affects the speed of the
# main thread. This is also why all buttons are on the same thread. This
# is a candidate for further investigation if there is time. 
def buttonThread():
    global wlight_colour
    global wlight_speed
    global wlight_pattern
    global button_press_count
    

    lock = threading.Lock()

    continue_thread = True
    
    canColourChange=0
    canSpeedChange=0
    canPatternChange=0
    
    count = 0
    
    # This changes the length of time the buttons are paused for. This 
    # will need to be calibrated.
    num_pause_steps = 20
    
    
    while continue_thread:
        count+=1
        
        
        #Temp taking keyboard input.
        key = getkey()
        print("Key: " + str(key))

        if key == "c":
            with lock:
                print("input c")
                new_colour_int = (wlight_colour.value + 1) % WColour.MAX.value
                wlight_colour = WColour(new_colour_int)

        elif key == "s":
            with lock:
                print("input s")
                new_speed_int = (wlight_speed.value + 1) % WSpeed.MAX.value
                wlight_speed = WSpeed(new_speed_int)

        elif key == "p":
            with lock:
                print("input p")
                new_pattern_int = (wlight_pattern.value + 1) % WPattern.MAX.value
                wlight_pattern = WPattern(new_pattern_int)
                
        elif key == "e":
            raise KeyboardInterrupt
                
        #End of temp
        
        ## Gather button inputs
        #inputColourButton = GPIO.input(colourInputPin)
        #inputSpeedValueButton = GPIO.input(speedInputPin)
        #inputPatternValueButton = GPIO.input(patternInputPin)
        
        ## Check which buttons are available.
        #colourButtonAvailable = canColourChange < count
        #speedButtonAvailable = canSpeedChange < count
        #patternButtonAvailable = canPatternChange < count
        
        ## Turn LEDs off if the buttons are available.
        #if colourButtonAvailable:
            #x=0 # Temp
            #GPIO.output(colourOutputPin, GPIO.LOW)
            
        #if speedButtonAvailable:
            #x=0 # Temp
            #GPIO.output(speedOutputPin, GPIO.LOW)
            
        #if patternButtonAvailable:
            #x=0 # Temp
            #GPIO.output(patternOutputPin, GPIO.LOW)
        
        ## For each button cycle the corresponding variable if the button
        ## has been pressed and it has not been pressed "recently"
        #if inputColourButton and colourButtonAvailable:
            #button_press_count += 1
            #canColourChange= count + num_pause_steps
            
            #with lock:
                #new_colour_int = (wlight_colour.value + 1) % WColour.MAX.value
                #wlight_colour = WColour(new_colour_int)
                ##wlogger.log_info("Button press - Colour, No. Presses: " + str(button_press_count))
                
            #if print_debug:
                #print("Button press - Colour", flush=True)
                #print(wlight_colour)
            #GPIO.output(colourOutputPin, GPIO.HIGH)
        

        #elif inputSpeedValueButton and speedButtonAvailable:
            #button_press_count += 1
            #canSpeedChange= count + num_pause_steps
            
            #with lock:
                #new_speed_int = (wlight_speed.value + 1) % WSpeed.MAX.value
                #wlight_speed = WSpeed(new_speed_int)
            
            #if print_debug:
                #print("Button press - Speed", flush=True)
                #print(wlight_speed)
            #GPIO.output(speedOutputPin, GPIO.HIGH)
            
        

        #elif inputPatternValueButton and patternButtonAvailable:
            #button_press_count += 1
            #canPatternChange = count + num_pause_steps
            
            #with lock:
                #new_pattern_int = (wlight_pattern.value + 1) % WPattern.MAX.value
                #wlight_pattern = WPattern(new_pattern_int)
            #if print_debug:
                #print("Button press - Pattern", flush=True)
                #print(wlight_pattern)
            #GPIO.output(patternOutputPin, GPIO.HIGH)

        
        # Small time delay between each run through. This does not
        # change the speed of the other thread as it is happens on
        # every loop.
        
        time.sleep(0.1)
        

input_thread = threading.Thread(target=buttonThread).start()



