import threading
import enum
import time
import random
import RPi.GPIO as GPIO
import Internals.Utils.wlogger as wlogger
import Main.config as config
import Main.enums as enums
import itertools
from random import randint

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
    
    
def randomly_change_pattern():
    # Randomly change colour, speed or pattern.
    variable_to_change = randint(0, 6)
    
    if variable_to_change == 0:
        # Change to other speed.

        with config.lock:
            config.wspeed_index = (config.wspeed_index + 1) % len(config.speedList)
                
        if print_debug:
            print("Auto Change - Speed", flush=True)
            print(config.speedList[config.wspeed_index], flush=True)
            
    elif variable_to_change < 4:
        # Change to random pattern.
        
        old_index = config.wpattern_index
        
        print("Pattern")
        
        with config.lock:
            while old_index == config.wpattern_index:
                config.wpattern_index = randint(0, len(config.patternList)-1)

        if print_debug:
            print("Auto Change - Pattern", flush=True)
            with config.lock:
                print(config.patternList[config.wpattern_index], flush=True)
            
    else:
        # Change to random colour.
        
        old_index = config.wcolour_index
        
        print("Colour")
        
        with config.lock:
            while old_index == config.wcolour_index:
                config.wcolour_index = randint(0, len(config.colourList)-1)

                
        if print_debug:
            print("Auto Change - Colour", flush=True)
            with config.lock:
                print(config.colourList[config.wcolour_index], flush=True)

def set_leds(canColourChange, canPatternChange, canSpeedChange, count):
    # Turn LEDs off if the buttons are available
    
    # + 5 has been tested and decided as a good length of time.
    if canColourChange < count  + 5:
        GPIO.output(config.colourOutputPin, GPIO.LOW)
    else:
        GPIO.output(config.colourOutputPin, GPIO.HIGH)
        
    if canSpeedChange < count  + 5:
        GPIO.output(config.speedOutputPin, GPIO.LOW)
    else:
        GPIO.output(config.speedOutputPin, GPIO.HIGH)
        
    if canPatternChange < count + 5:
        GPIO.output(config.patternOutputPin, GPIO.LOW)
    else:
        GPIO.output(config.patternOutputPin, GPIO.HIGH)


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
    input_thread = threading.currentThread()

    continue_thread = True
    
    canColourChange=0
    canSpeedChange=0
    canPatternChange=0
    
    count = 0
    

    while not input_thread.stopped():
        # Increment the cycle count.
        count+=1
        
        # Determine if the brightness needs changing by looking at the number
        # of cycles there has been without a button press.
        if config.cycles_without_button_press == config.num_cycles_before_dimming:
            with config.lock:
                config.current_brightness = config.NIGHT_BRIGHTNESS
                if print_debug:
                    print("Night Brightness: " + str(count))
        elif config.cycles_without_button_press == 0:
            with config.lock:
                if print_debug:
                    print("Day Brightness: " + str(count))
                config.current_brightness = config.MAX_BRIGHTNESS
        
        # Assume this cycles has no button press. This will be reset to
        # zero if a button is pressed.
        config.cycles_without_button_press += 1

        # Determine whether a random change is needed. 
        
        if config.cycles_without_button_press > config.num_cycles_before_random_changes \
            and config.cycles_without_button_press % config.random_change_frequency == 0:
            
            if print_debug:
                    print("Random Change: " + str(count))
            randomly_change_pattern()
                

        ## Gather button inputs
        inputColourButton = GPIO.input(config.colourInputPin)
        inputSpeedValueButton = GPIO.input(config.speedInputPin)
        inputPatternValueButton = GPIO.input(config.patternInputPin)
        
        # Check which buttons are available.
        colourButtonAvailable = canColourChange < count
        speedButtonAvailable = canSpeedChange < count
        patternButtonAvailable = canPatternChange < count
        
        # Set LEDs correctly
        set_leds(canColourChange, canPatternChange, canSpeedChange, count)
        
        
        # For each button cycle the corresponding variable if the button
        # has been pressed and it has not been pressed "recently"
        if inputColourButton and colourButtonAvailable:
            config.cycles_without_button_press = 0
            button_press_count += 1
            canColourChange= count + config.pause_cycles
            
            with config.lock:
                config.wcolour_index = (config.wcolour_index + 1) % len(config.colourList)
                wlogger.log_info("Button press - Colour, No. Presses: " + str(button_press_count))
                
                if print_debug:
                    print("Button press - Colour", flush=True)
                    print(config.colourList[config.wcolour_index])
                    print("Count: " + str(count))
                
            GPIO.output(config.colourOutputPin, GPIO.HIGH)
        

        elif inputSpeedValueButton and speedButtonAvailable:
            config.cycles_without_button_press = 0
            button_press_count += 1
            canSpeedChange= count + config.pause_cycles
            
            with config.lock:
                config.wspeed_index = (wspeed_index + 1) % config.wspeed_index
            
                if print_debug:
                    print("Button press - Speed", flush=True)
                    print(config.speedList[config.wspeed_index])
                
            GPIO.output(config.speedOutputPin, GPIO.HIGH)
            
        

        elif inputPatternValueButton and patternButtonAvailable:
            config.cycles_without_button_press = 0
            button_press_count += 1
            canPatternChange = count + config.pause_cycles
            
            with config.lock:
                config.wpattern_index = (config.wpattern_index + 1) % len(config.patternList)
                if print_debug:
                    print("Button press - Pattern", flush=True)
                    print(config.patternList[config.wpattern_index])
                
            GPIO.output(config.patternOutputPin, GPIO.HIGH)

        
        # Small time delay between each run through. This does not
        # change the speed of the other thread as it is happens on
        # every loop.
        
        time.sleep(0.1)
        

#
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

