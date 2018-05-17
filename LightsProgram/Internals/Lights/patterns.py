""" This file holds all the different patterns that can be used"""
import Main.config as config
import Main.enums as enums
from Internals.Lights.colourcycletemplate import ColorCycleTemplate
import Internals.Utils.wlogger as wlogger
import math

print_debug = True


def slide(strip, num_steps_per_cycle, current_step, current_cycle, slide_speed, *args):
    """ This function turns the LEDs on one at a time until all in the given
    block are done."""
        
    if len(args) == 0:
        return
        

    current_colour = args[0].get_colour()
    current_speed = args[0].get_speed()

    if print_debug: 
        print("----------------------------")
        print("Slide")
        print(current_colour)
        print(current_speed)

    
    # Calculate total number of LEDs
    total_num_leds = 0
    for block in args:
        block_num_leds = block.get_end_index() - block.get_start_index()
        total_num_leds += block_num_leds
        
    # Number of LEDs to turn on is stored on the blocks. This means it
    # stays the same when the speed is changed.
    
    num_leds_on = math.ceil(args[0].get_pattern_index())

    # Calibrate this once on the dog.

    if current_speed == enums.WSpeed.Sloth:
        num_steps_per_slide = slide_speed*3
    elif current_speed == enums.WSpeed.Hare:
        num_steps_per_slide = slide_speed*2
    else: #enums.WSpeed.Cheetah:
        num_steps_per_slide = slide_speed

    # The index of the LED within the current blocks.
    local_led_index = 0
    
    for block in args:
        for led in range(block.get_start_index(), block.get_end_index()):

            if local_led_index <= num_leds_on:
                # Paint single LEDS with given colour
                strip.set_pixel(led, math.floor(enums.colourDi[current_colour][0]*255),
                           math.floor(enums.colourDi[current_colour][1]*255),
                           math.floor(enums.colourDi[current_colour][2]*255), 
                           config.MAX_BRIGHTNESS)
            else:
                # Paint gap LED black.
                strip.set_pixel(led, 0.0, 0.0, 0.0)
                
            local_led_index += 1
            
    # Work out the number of extra leds needed on next run through.
    num_leds_per_step = total_num_leds/num_steps_per_slide
    args[0].increment_pattern_index(num_leds_per_step)
    
    # Set to zero after we have filled up the strip. (1.5 is needed to account for
    # numerical precision errors). 
    if(args[0].get_pattern_index() > total_num_leds + num_leds_per_step*1.5):
        args[0].set_pattern_index(0)

    info_string = "Pattern: Slide. Colour: " + str(current_colour) + ". Speed: " \
                  + str(current_speed)
    wlogger.log_info(info_string)
    wlogger.log_info(strip.leds)
    
def rainbow_slide(strip, num_steps_per_cycle, current_step, current_cycle, slide_speed, *args):
    """ This function turns the LEDs on one at a time until all in the given
    block are done."""
        
    if len(args) == 0:
        return
        
        
    if print_debug: 
        print("----------------------------")
        print("Rainbow Slide")
        
    pixel_color = strip.wheel(math.floor(current_step/2 % 255))
    current_speed = args[0].get_speed()
    
    # Calculate total number of LEDs
    total_num_leds = 0
    for block in args:
        block_num_leds = block.get_end_index() - block.get_start_index()
        total_num_leds += block_num_leds
        
    # Number of LEDs to turn on is stored on the blocks. This means it
    # stays the same when the speed is changed.
    
    num_leds_on = math.ceil(args[0].get_pattern_index())

    # Calibrate this once on the dog.

    if current_speed == enums.WSpeed.Sloth:
        num_steps_per_slide = slide_speed*3
    elif current_speed == enums.WSpeed.Hare:
        num_steps_per_slide = slide_speed*2
    else: #enums.WSpeed.Cheetah:
        num_steps_per_slide = slide_speed

    # The index of the LED within the current blocks.
    local_led_index = 0
    
    for block in args:
        for led in range(block.get_start_index(), block.get_end_index()):

            if local_led_index <= num_leds_on:
                # Paint single LEDS with given colour
                strip.set_pixel_rgb(led, pixel_color, config.MAX_BRIGHTNESS/2)
            else:
                # Paint gap LED black.
                strip.set_pixel(led, 0.0, 0.0, 0.0)
                
            local_led_index += 1
            
    # Work out the number of extra leds needed on next run through.
    num_leds_per_step = total_num_leds/num_steps_per_slide
    args[0].increment_pattern_index(num_leds_per_step)
    
    # Set to zero after we have filled up the strip. (1.5 is needed to account for
    # numerical precision errors). 
    if(args[0].get_pattern_index() > total_num_leds + num_leds_per_step*1.5):
        args[0].set_pattern_index(0)

    info_string = "Pattern: RainbowSlide. Colour: " + str(pixel_color) 
    wlogger.log_info(info_string)
        
        
def singles(strip, num_steps_per_cycle, current_step, current_cycle, *args):
    """ This function moves single LEDs along the LED strip indices given"""
        
    if not args:
        return
        
    single_gap = 9

    current_colour = args[0].get_colour()
    current_speed = args[0].get_speed()

        
    if print_debug: 
        print("----------------------------")
        print("Singles")
        print(current_speed)
        print(current_colour)

    # Pattern specific behaviour
    pattern_speed_factor = 1
    num_steps_per_pattern_step = enums.speedDi[current_speed]*pattern_speed_factor

    # The index of the LED within the current blocks.
    local_led_index = 0
    
    for block in args:
        for led in range(block.get_start_index(), block.get_end_index()):
            if (local_led_index + args[0].get_pattern_index()) % (single_gap + 1) == 0:
                # Paint single LEDS with given colour
                strip.set_pixel(led, math.floor(enums.colourDi[current_colour][0]*255),
                           math.floor(enums.colourDi[current_colour][1]*255),
                           math.floor(enums.colourDi[current_colour][2]*255), 
                           config.MAX_BRIGHTNESS)
            else:
                # Paint gap LED black.
                strip.set_pixel(led, 0.0, 0.0, 0.0)
                
            local_led_index += 1
    
    if(current_step % num_steps_per_pattern_step == 0):
        args[0].increment_pattern_index(1)

    info_string = "Pattern: Singles. Colour: " + str(current_colour) + ". Speed: " \
                  + str(current_speed)
    wlogger.log_info(info_string)
    wlogger.log_info(strip.leds)
    
def snakes(strip, num_steps_per_cycle, current_step, current_cycle, *args):
    """ This function moves single LEDs along the LED strip indices given"""
        
    if not args:
        return
        
    snake_length = 15
    snake_gap = 30

    current_colour = args[0].get_colour()
    current_speed = args[0].get_speed()

        
    if print_debug: 
        print("----------------------------")
        print("Snakes")
        print(current_speed)
        print(current_colour)

    # Pattern specific behaviour
    pattern_speed_factor = 1
    num_steps_per_pattern_step = enums.speedDi[current_speed]*pattern_speed_factor

    # The index of the LED within the current blocks.
    local_led_index = 0
    
    for block in args:
        for led in range(block.get_start_index(), block.get_end_index()):
            if (local_led_index + args[0].get_pattern_index()) % (snake_length + snake_gap) < snake_length:
                # Paint snake LEDS with given colour
                strip.set_pixel(led, math.floor(enums.colourDi[current_colour][0]*255),
                           math.floor(enums.colourDi[current_colour][1]*255),
                           math.floor(enums.colourDi[current_colour][2]*255), 
                           config.MAX_BRIGHTNESS)
            else:
                # Paint gap LED black.
                strip.set_pixel(led, 0.0, 0.0, 0.0)
                
            local_led_index += 1
    
    if(current_step % num_steps_per_pattern_step == 0):
        args[0].increment_pattern_index(1)

    info_string = "Pattern: Snakes. Colour: " + str(current_colour) + ". Speed: " \
                  + str(current_speed)
    wlogger.log_info(info_string)
    wlogger.log_info(strip.leds)
    
def renishaw(strip, num_steps_per_cycle, current_step, current_cycle, *args):
    """ This function moves Renishaw in morse code along the LED strip indices given"""
        
    if not args:
        return
        
    renishaw_morse_code = [ 1,0,1,1,1,0,1,
                            0,0,0,0,0,
                            1,
                            0,0,0,0,0,
                            1,1,1,0,1,0,
                            0,0,0,0,0,
                            1,0,1,
                            0,0,0,0,0,
                            1,0,1,0,1,
                            0,0,0,0,0,
                            1,0,1,0,1,0,1,
                            0,0,0,0,0,
                            1,0,1,1,1,
                            0,0,0,0,0,
                            1,0,1,1,1,0,1,1,1,
                            0,0,0,0,0,
                            0,0,0,0,0,
                            0,0,0,0,0,
                            0,0,0,0,0]
                            

    current_colour = args[0].get_colour()
    current_speed = args[0].get_speed()

        
    if print_debug: 
        print("----------------------------")
        print("Renishaw Morse")
        print(current_speed)
        print(current_colour)

    # Pattern specific behaviour
    pattern_speed_factor = 2
    num_steps_per_pattern_step = enums.speedDi[current_speed]*pattern_speed_factor

    # The index of the LED within the current blocks.
    local_led_index = 0
    
    for block in args:
        for led in range(block.get_start_index(), block.get_end_index()):

            if renishaw_morse_code[(local_led_index + args[0].get_pattern_index()) % len(renishaw_morse_code)]:
                # Paint snake LEDS with given colour
                strip.set_pixel(led, math.floor(enums.colourDi[current_colour][0]*255),
                           math.floor(enums.colourDi[current_colour][1]*255),
                           math.floor(enums.colourDi[current_colour][2]*255), 
                           config.MAX_BRIGHTNESS)
            else:
                # Paint gap LED black.
                strip.set_pixel(led, 0.0, 0.0, 0.0)
                
            local_led_index += 1
    
    if(current_step % num_steps_per_pattern_step == 0):
        args[0].increment_pattern_index(1)

    info_string = "Pattern: Renishaw Morse. Colour: " + str(current_colour) + ". Speed: " \
                  + str(current_speed)
    wlogger.log_info(info_string)
    wlogger.log_info(strip.leds)

def all_on(strip, *args):
    """ This function turns the LEDs on one at a time until all in the given
    block are done."""
        
    if not args:
        return

    current_colour = args[0].get_colour()
    
    if print_debug: 
        print("----------------------------")
        print("All On")
        print(current_colour)


    # The index of the LED within the current blocks.
    local_led_index = 0
    
    for block in args:
        for led in range(block.get_start_index(), block.get_end_index()):
            
            # Paint single LEDS with given colour
            strip.set_pixel(led, math.floor(enums.colourDi[current_colour][0]*255),
                           math.floor(enums.colourDi[current_colour][1]*255),
                           math.floor(enums.colourDi[current_colour][2]*255),
                           config.MAX_BRIGHTNESS)


            local_led_index += 1

    info_string = "Pattern: All On. Colour: " + str(current_colour)
    wlogger.log_info(info_string)
    wlogger.log_info(strip.leds)
