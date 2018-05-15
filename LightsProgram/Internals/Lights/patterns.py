""" This file holds all the different patterns that can be used"""
import Main.config as config
import Main.enums as enums
from Internals.Lights.colourcycletemplate import ColorCycleTemplate
import Internals.Utils.wlogger as wlogger
import math

print_debug = True


def slide(strip, num_steps_per_cycle, current_step, current_cycle, *args):
    """ This function turns the LEDs on one at a time until all in the given
    block are done."""
        
    if len(args) == 0:
        return
        
    current_colour = args[0].local_colour
    current_speed = args[0].local_speed

        
    if print_debug: 
        print("----------------------------")
        print("Slide")
        print(current_colour)

    
    # Calculate total number of LEDs
    total_num_leds = 0
    for block in args:
        block_num_leds = block.end_index - block.start_index
        total_num_leds += block_num_leds
        
    # Calculate number of LEDs to turn on based on how through the
    # current cycle we are. (This is more accurate than calculating 
    # a set step) This ensures we start with no LEDs on and end with
    # them all on.
    
    num_leds_on = math.ceil((total_num_leds/num_steps_per_cycle)*current_step)

    # The index of the LED within the current blocks.
    local_led_index = 0
    
    for block in args:
        for led in range(block.start_index, block.end_index):

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

    info_string = "Pattern: Slide. Colour: " + str(current_colour) + ". Speed: " \
                  + str(current_speed)
    wlogger.log_info(info_string)
    wlogger.log_info(strip.leds)
        
        
def singles(strip, num_steps_per_cycle, current_step, current_cycle, *args):
    """ This function moves single LEDs along the LED strip indices given"""
        
    if not args:
        return
        
    single_gap = 9

    current_colour = args[0].local_colour
    current_speed = args[0].local_speed

        
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
        for led in range(block.start_index, block.end_index):
            pattern_step = math.floor(current_step/num_steps_per_pattern_step)

            if (local_led_index + pattern_step) % (single_gap + 1) == 0:
                # Paint single LEDS with given colour
                strip.set_pixel(led, math.floor(enums.colourDi[current_colour][0]*255),
                           math.floor(enums.colourDi[current_colour][1]*255),
                           math.floor(enums.colourDi[current_colour][2]*255), 
                           config.MAX_BRIGHTNESS)
                print("Local LED number: " + str(local_led_index))
                print("LED number: " + str(led))
            else:
                # Paint gap LED black.
                strip.set_pixel(led, 0.0, 0.0, 0.0)
                
            local_led_index += 1

    info_string = "Pattern: Slide. Colour: " + str(current_colour) + ". Speed: " \
                  + str(current_speed)
    wlogger.log_info(info_string)
    wlogger.log_info(strip.leds)

def all_on(strip, *args):
    """ This function turns the LEDs on one at a time until all in the given
    block are done."""
        
    if not args:
        return

    current_colour = args[0].colour
    current_speed = args[0].speed

        
    if print_debug: 
        print("----------------------------")
        print("All On")
        print(current_speed)
        print(current_colour)


    # The index of the LED within the current blocks.
    local_led_index = 0
    
    for block in args:
        for led in range(block.start_index, block.end_index):
            
            # Paint single LEDS with given colour
            strip.set_pixel(led, math.floor(wevents.colourDi[current_colour][0]*255),
                           math.floor(wevents.colourDi[current_colour][1]*255),
                           math.floor(wevents.colourDi[current_colour][2]*255), 
                           config.MAX_BRIGHTNESS)
                           
            print("Local LED number: " + str(local_led_index))
            print("LED number: " + str(led))

            local_led_index += 1

    info_string = "Pattern: All On. Colour: " + str(current_colour) + ". Speed: " \
                  + str(current_speed)
    wlogger.log_info(info_string)
    wlogger.log_info(strip.leds)
