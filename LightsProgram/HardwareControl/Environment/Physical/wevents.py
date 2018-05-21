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
    
    
def randomly_change_pattern(lock, colour_cycle, speed_cycle, pattern_cycle):
    # Randomly change colour, speed or pattern.
    variable_to_change = randint(0, 2)
    
    if variable_to_change == 0:
        # Cycle a random number of times.
        number_of_cycles = randint(1, len(config.speedList)-1)
        
        for cycle in range(0, number_of_cycles):
            with lock:
                config.wlight_speed = next(speed_cycle)
                
        if print_debug:
            print("Auto Change - Speed", flush=True)
            print(config.wlight_speed, flush=True)
            
    elif variable_to_change == 1:
        # Cycle a random number of times.
        number_of_cycles = randint(1, len(config.patternList)-1)
        
        for cycle in range(0, number_of_cycles):
            with lock:
                config.wlight_pattern = next(pattern_cycle)
                
        if print_debug:
            print("Auto Change - Pattern", flush=True)
            print(config.wlight_pattern, flush=True)
            
    elif variable_to_change == 2:
        # Cycle a random number of times.
        number_of_cycles = randint(1, len(config.colourList)-1)
        
        for cycle in range(0, number_of_cycles):
            with lock:
                config.wlight_colour = next(colour_cycle)
                
        if print_debug:
            print("Auto Change - Colour", flush=True)
            print(config.wlight_colour, flush=True)

def set_leds(canColourChange, canPatternChange, canSpeedChange, count):
    # Turn LEDs off if the buttons are available
    
    # + 10 is untested as LEDs not currently responsive. 
    if canColourChange < count  + 10:
        GPIO.output(config.colourOutputPin, GPIO.LOW)
        
    if canSpeedChange < count  + 10:
        GPIO.output(config.speedOutputPin, GPIO.LOW)
        
    if canPatternChange < count + 10:
        GPIO.output(config.patternOutputPin, GPIO.LOW)


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

    lock = threading.Lock()

    continue_thread = True
    
    canColourChange=0
    canSpeedChange=0
    canPatternChange=0
    
    count = 0
    
    pattern_cycle = itertools.cycle(config.patternList)
    colour_cycle = itertools.cycle(config.colourList)
    speed_cycle = itertools.cycle(config.speedList)
    
    with lock:
        config.wlight_pattern = next(pattern_cycle)
        config.wlight_colour = next(colour_cycle)
        config.wlight_speed = next(speed_cycle)
    
    
    while not input_thread.stopped():
        # Increment the cycle count.
        count+=1
        print(count)
        
        # Determine if the brightness needs changing by looking at the number
        # of cycles there has been without a button press.
        if config.cycles_without_button_press == config.num_cycles_before_dimming:
            with lock:
                config.current_brightness = config.NIGHT_BRIGHTNESS
        elif config.cycles_without_button_press == 0:
            with lock:
                config.current_brightness = config.MAX_BRIGHTNESS
        
        # Assume this cycles has no button press. This will be reset to
        # zero if a button is pressed.
        config.cycles_without_button_press += 1
        
        
        # Determine whether a random change is needed. 
        
        if config.cycles_without_button_press > config.num_cycles_before_random_changes \
            and config.cycles_without_button_press % config.random_change_frequency == 0:
            
            randomly_change_pattern(lock, colour_cycle, speed_cycle, pattern_cycle)
                

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
            
            with lock:
                config.wlight_colour = next(colour_cycle)
                #wlogger.log_info("Button press - Colour, No. Presses: " + str(button_press_count))
                
                if print_debug:
                    print("Button press - Colour", flush=True)
                    print(config.wlight_colour)
                    print("Count: " + str(count))
                
            GPIO.output(config.colourOutputPin, GPIO.HIGH)
        

        elif inputSpeedValueButton and speedButtonAvailable:
            config.cycles_without_button_press = 0
            button_press_count += 1
            canSpeedChange= count + config.pause_cycles
            
            with lock:
                config.wlight_speed = next(speed_cycle)
            
                if print_debug:
                    print("Button press - Speed", flush=True)
                    print(config.wlight_speed)
                
            GPIO.output(config.speedOutputPin, GPIO.HIGH)
            
        

        elif inputPatternValueButton and patternButtonAvailable:
            config.cycles_without_button_press = 0
            button_press_count += 1
            canPatternChange = count + config.pause_cycles
            
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



