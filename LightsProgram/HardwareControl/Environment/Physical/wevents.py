import threading
import enum
import time
import random
import RPi.GPIO as GPIO
import Internals.Utils.wlogger as wlogger
import Main.config as config
import Main.enums as enums
from itertools import cycle

import termios
import sys
import tty
#from msvcrt import getwch

print_debug = True


def set_up_pins():
    GPIO.setwarnings(False)
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(config.colourInputPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(config.speedInputPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(config.patternInputPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    GPIO.setup(config.colourOutputPin, GPIO.OUT)
    GPIO.setup(config.speedOutputPin, GPIO.OUT)
    GPIO.setup(config.patternOutputPin, GPIO.OUT)





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
    global button_press_count
    

    lock = threading.Lock()

    continue_thread = True
    
    canColourChange=0
    canSpeedChange=0
    canPatternChange=0
    
    count = 0
    
    pattern_cycle = cycle(config.patternList)
    with lock:
        config.wlight_pattern = next(pattern_cycle)
    
    # This changes the length of time the buttons are paused for. This 
    # will need to be calibrated.
    num_pause_steps = config.pause_cycles
    
    
    while continue_thread:
        count+=1
        
        
        #Temp taking keyboard input.
        #key = getkey()
        #print("Key: " + str(key))

        #if key == "c":
            #with lock:
                #print("input c")
                #new_colour_int = (wlight_colour.value + 1) % WColour.MAX.value
                #wlight_colour = WColour(new_colour_int)

        #elif key == "s":
            #with lock:
                #print("input s")
                #new_speed_int = (wlight_speed.value + 1) % WSpeed.MAX.value
                #wlight_speed = WSpeed(new_speed_int)

        #elif key == "p":
            #with lock:
                #print("input p")
                #new_pattern_int = (wlight_pattern.value + 1) % WPattern.MAX.value
                #wlight_pattern = WPattern(new_pattern_int)
                
        #elif key == "e":
            #raise KeyboardInterrupt
                
        #End of temp
        
        ## Gather button inputs
        inputColourButton = GPIO.input(config.colourInputPin)
        inputSpeedValueButton = GPIO.input(config.speedInputPin)
        inputPatternValueButton = GPIO.input(config.patternInputPin)
        
        # Check which buttons are available.
        colourButtonAvailable = canColourChange < count
        speedButtonAvailable = canSpeedChange < count
        patternButtonAvailable = canPatternChange < count
        
        # Turn LEDs off if the buttons are available.
        if colourButtonAvailable:
            x=0 # Temp
            GPIO.output(config.colourOutputPin, GPIO.LOW)
            
        if speedButtonAvailable:
            x=0 # Temp
            GPIO.output(config.speedOutputPin, GPIO.LOW)
            
        if patternButtonAvailable:
            x=0 # Temp
            GPIO.output(config.patternOutputPin, GPIO.LOW)
        
        # For each button cycle the corresponding variable if the button
        # has been pressed and it has not been pressed "recently"
        if inputColourButton and colourButtonAvailable:
            button_press_count += 1
            canColourChange= count + num_pause_steps
            
            with lock:
                new_colour_int = (config.wlight_colour.value + 1) % enums.WColour.MAX.value
                config.wlight_colour = enums.WColour(new_colour_int)
                #wlogger.log_info("Button press - Colour, No. Presses: " + str(button_press_count))
                
            if print_debug:
                print("Button press - Colour", flush=True)
                print(config.wlight_colour)
                
            GPIO.output(config.colourOutputPin, GPIO.HIGH)
        

        elif inputSpeedValueButton and speedButtonAvailable:
            button_press_count += 1
            canSpeedChange= count + num_pause_steps
            
            with lock:
                new_speed_int = (config.wlight_speed.value + 1) % enums.WSpeed.MAX.value
                config.wlight_speed = enums.WSpeed(new_speed_int)
            
            if print_debug:
                print("Button press - Speed", flush=True)
                print(config.wlight_speed)
                
            GPIO.output(config.speedOutputPin, GPIO.HIGH)
            
        

        elif inputPatternValueButton and patternButtonAvailable:
            button_press_count += 1
            canPatternChange = count + num_pause_steps
            
            
            with lock:
                config.wlight_pattern = next(pattern_cycle)
                config.pattern_position_index = 0
            if print_debug:
                print("Button press - Pattern", flush=True)
                print(config.wlight_pattern)
                
            GPIO.output(config.patternOutputPin, GPIO.HIGH)

        
        # Small time delay between each run through. This does not
        # change the speed of the other thread as it is happens on
        # every loop.
        
        time.sleep(0.1)
        





