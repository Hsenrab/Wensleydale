""" This file holds all the different patterns that can be used"""
import Main.config as config
import Main.enums as enums
from Internals.Lights.colourcycletemplate import ColorCycleTemplate
import Internals.Utils.wlogger as wlogger
import math
import numpy as np
print_debug = False


def slide(strip, num_steps_per_cycle, current_step, current_cycle, slide_speed, blockList):
    """ This function turns the LEDs on one at a time until all in the given
    block are done."""
        
    if len(blockList) == 0:
        return
        

    current_colour = blockList[0].get_colour()
    current_speed = blockList[0].get_speed()

    if print_debug: 
        print("----------------------------")
        print("Slide")
        print(current_colour)
        print(current_speed)
        print(config.current_brightness)

    
    # Calculate total number of LEDs
    total_num_leds = 0
    for block in blockList:
        block_num_leds = block.get_end_index() - block.get_start_index()
        total_num_leds += block_num_leds
        
    # Number of LEDs to turn on is stored on the blocks. This means it
    # stays the same when the speed is changed.
    
    num_leds_on = math.ceil(blockList[0].get_pattern_index())

    # Calibrate this once on the dog.

    if current_speed == enums.WSpeed.Sloth:
        num_steps_per_slide = slide_speed*3
    elif current_speed == enums.WSpeed.Hare:
        num_steps_per_slide = slide_speed*2
    else: #enums.WSpeed.Cheetah:
        num_steps_per_slide = slide_0speed

    # The index of the LED within the current blocks.
    local_led_index = 0
    
    for block in blockList:
        
        if block.get_direction():
            ledList = np.arange(block.get_end_index(), block.get_start_index(), -1)
        else:
            ledList = np.arange(block.get_start_index(), block.get_end_index())
            
        for led in ledList:

            if local_led_index <= num_leds_on:
                # Paint single LEDS with given colour
                strip.set_pixel(led, math.floor(enums.colourDi[current_colour][0]*255),
                           math.floor(enums.colourDi[current_colour][1]*255),
                           math.floor(enums.colourDi[current_colour][2]*255), 
                           config.current_brightness)
            else:
                # Paint gap LED black.
                strip.set_pixel(led, 0.0, 0.0, 0.0)
                
            local_led_index += 1
            
    # Work out the number of extra leds needed on next run through.
    num_leds_per_step = total_num_leds/num_steps_per_slide
    blockList[0].increment_pattern_index(num_leds_per_step)
    
    # Set to zero after we have filled up the strip. (1.5 is needed to account for
    # numerical precision errors). 
    if(blockList[0].get_pattern_index() > total_num_leds + num_leds_per_step*1.5):
        blockList[0].set_pattern_index(0)

    info_string = "Pattern: Slide. Colour: " + str(current_colour) + ". Speed: " \
                  + str(current_speed)
    wlogger.log_info(info_string)
    wlogger.log_info(strip.leds)
    
def rainbow_slide(strip, num_steps_per_cycle, current_step, current_cycle, slide_speed, blockList):
    """ This function turns the LEDs on one at a time until all in the given
    block are done."""
        
    if len(blockList) == 0:
        return
        
        
    if print_debug: 
        print("----------------------------")
        print("Rainbow Slide")
        print(config.current_brightness)
        
    pixel_color = strip.wheel(math.floor(current_step/2 % 255))
    current_speed = blockList[0].get_speed()
    
    # Calculate total number of LEDs
    total_num_leds = 0
    for block in blockList:
        block_num_leds = block.get_end_index() - block.get_start_index()
        total_num_leds += block_num_leds
        
    # Number of LEDs to turn on is stored on the blocks. This means it
    # stays the same when the speed is changed.
    
    num_leds_on = math.ceil(blockList[0].get_pattern_index())

    # Calibrate this once on the dog.

    if current_speed == enums.WSpeed.Sloth:
        num_steps_per_slide = slide_speed*3
    elif current_speed == enums.WSpeed.Hare:
        num_steps_per_slide = slide_speed*2
    else: #enums.WSpeed.Cheetah:
        num_steps_per_slide = slide_speed

    # The index of the LED within the current blocks.
    local_led_index = 0
    
    for block in blockList:
                
        if block.get_direction():
            ledList = np.arange(block.get_end_index(), block.get_start_index(), -1)
        else:
            ledList = np.arange(block.get_start_index(), block.get_end_index())
            
        for led in ledList:

            if local_led_index <= num_leds_on:
                # Paint single LEDS with given colour
                strip.set_pixel_rgb(led, pixel_color, config.current_brightness/2)
            else:
                # Paint gap LED black.
                strip.set_pixel(led, 0.0, 0.0, 0.0)
                
            local_led_index += 1
            
    # Work out the number of extra leds needed on next run through.
    num_leds_per_step = total_num_leds/num_steps_per_slide
    blockList[0].increment_pattern_index(num_leds_per_step)
    
    # Set to zero after we have filled up the strip. (1.5 is needed to account for
    # numerical precision errors). 
    if(blockList[0].get_pattern_index() > total_num_leds + num_leds_per_step*1.5):
        blockList[0].set_pattern_index(0)

    info_string = "Pattern: RainbowSlide. Colour: " + str(pixel_color) 
    wlogger.log_info(info_string)
        
        
def singles(strip, num_steps_per_cycle, current_step, current_cycle, blockList):
    """ This function moves single LEDs along the LED strip indices given"""
        
    if not blockList:
        return
        
    single_gap = 9

    current_colour = blockList[0].get_colour()
    current_speed = blockList[0].get_speed()

        
    if print_debug: 
        print("----------------------------")
        print("Singles")
        print(current_speed)
        print(current_colour)
        print(config.current_brightness)

    # Pattern specific behaviour
    pattern_speed_factor = 1
    num_steps_per_pattern_step = enums.speedDi[current_speed]*pattern_speed_factor

    # The index of the LED within the current blocks.
    local_led_index = 0
    
    for block in blockList:
        if block.get_direction():
            ledList = np.arange(block.get_end_index(), block.get_start_index(), -1)
        else:
            ledList = np.arange(block.get_start_index(), block.get_end_index())
            
        for led in ledList:
            if (local_led_index + blockList[0].get_pattern_index()) % (single_gap + 1) == 0:
                # Paint single LEDS with given colour
                strip.set_pixel(led, math.floor(enums.colourDi[current_colour][0]*255),
                           math.floor(enums.colourDi[current_colour][1]*255),
                           math.floor(enums.colourDi[current_colour][2]*255), 
                           config.current_brightness)
            else:
                # Paint gap LED black.
                strip.set_pixel(led, 0.0, 0.0, 0.0)
                
            local_led_index += 1
    
    if(current_step % num_steps_per_pattern_step == 0):
        blockList[0].increment_pattern_index(1)

    info_string = "Pattern: Singles. Colour: " + str(current_colour) + ". Speed: " \
                  + str(current_speed) + ". Brightness: " + str(config.current_brightness)
    wlogger.log_info(info_string)
    wlogger.log_info(strip.leds)
    
def snakes(strip, num_steps_per_cycle, current_step, current_cycle, blockList):
    """ This function moves single LEDs along the LED strip indices given"""
        
    if not blockList:
        return
        
    snake_length = 15
    snake_gap = 30

    current_colour = blockList[0].get_colour()
    current_speed = blockList[0].get_speed()

        
    if print_debug: 
        print("----------------------------")
        print("Snakes")
        print(current_speed)
        print(current_colour)
        print(config.current_brightness)

    # Pattern specific behaviour
    pattern_speed_factor = 1
    num_steps_per_pattern_step = enums.speedDi[current_speed]*pattern_speed_factor

    # The index of the LED within the current blocks.
    local_led_index = 0
    
    for block in blockList:
        if block.get_direction():
            ledList = np.arange(block.get_end_index(), block.get_start_index(), -1)
        else:
            ledList = np.arange(block.get_start_index(), block.get_end_index())
            
        for led in ledList:
            if (local_led_index + blockList[0].get_pattern_index()) % (snake_length + snake_gap) < snake_length:
                # Paint snake LEDS with given colour
                strip.set_pixel(led, math.floor(enums.colourDi[current_colour][0]*255),
                           math.floor(enums.colourDi[current_colour][1]*255),
                           math.floor(enums.colourDi[current_colour][2]*255), 
                           config.current_brightness)
            else:
                # Paint gap LED black.
                strip.set_pixel(led, 0.0, 0.0, 0.0)
                
            local_led_index += 1
    
    if(current_step % num_steps_per_pattern_step == 0):
        print(current_step)
        blockList[0].increment_pattern_index(1)

    info_string = "Pattern: Snakes. Colour: " + str(current_colour) + ". Speed: " \
                  + str(current_speed) + ". Brightness: " + str(config.current_brightness)
    wlogger.log_info(info_string)
    wlogger.log_info(strip.leds)
    
def moving_morse(strip, num_steps_per_cycle, current_step, current_cycle, morse, blockList):
    """ This function moves Renishaw in morse code along the LED strip indices given"""
        
    if not blockList:
        return


    current_colour = blockList[0].get_colour()
    current_speed = blockList[0].get_speed()

        
    if print_debug: 
        print("----------------------------")
        print("Moving Morse")
        print(current_speed)
        print(current_colour)
        print(config.current_brightness)

    # Pattern specific behaviour
    pattern_speed_factor = 2
    num_steps_per_pattern_step = enums.speedDi[current_speed]*pattern_speed_factor

    # The index of the LED within the current blocks.
    local_led_index = 0
    
    for block in blockList:
        if block.get_direction():
            ledList = np.arange(block.get_end_index(), block.get_start_index(), -1)
        else:
            ledList = np.arange(block.get_start_index(), block.get_end_index())
            
        for led in ledList:

            if morse[(local_led_index + blockList[0].get_pattern_index()) % len(morse)]:
                # Paint snake LEDS with given colour
                strip.set_pixel(led, math.floor(enums.colourDi[current_colour][0]*255),
                           math.floor(enums.colourDi[current_colour][1]*255),
                           math.floor(enums.colourDi[current_colour][2]*255), 
                           config.current_brightness)
            else:
                # Paint gap LED black.
                strip.set_pixel(led, 0.0, 0.0, 0.0)
                
            local_led_index += 1
    
    if(current_step % num_steps_per_pattern_step == 0):
        blockList[0].increment_pattern_index(1)

    info_string = "Pattern: Renishaw Morse. Colour: " + str(current_colour) + ". Speed: " \
                  + str(current_speed) + ". Brightness: " + str(config.current_brightness)
    wlogger.log_info(info_string)
    wlogger.log_info(strip.leds)
    
    
def fixed_morse(strip, num_steps_per_cycle, current_step, current_cycle, morse, blockList):
    """ This function moves Renishaw in morse code along the LED strip indices given"""
        
    if not blockList:
        return


    current_colour = blockList[0].get_colour()

        
    if print_debug: 
        print("----------------------------")
        print("Fixed Morse")
        print(current_colour)
        print(config.current_brightness)


    # The index of the LED within the current blocks.
    local_led_index = 0
    
    for block in blockList:
        
        if block.get_direction():
            ledList = np.arange(block.get_end_index(), block.get_start_index(), -1)
        else:
            ledList = np.arange(block.get_start_index(), block.get_end_index())
            
        for led in ledList:
            if local_led_index < len(morse) and morse[local_led_index]:
                # Paint snake LEDS with given colour
                strip.set_pixel(led, math.floor(enums.colourDi[current_colour][0]*255),
                           math.floor(enums.colourDi[current_colour][1]*255),
                           math.floor(enums.colourDi[current_colour][2]*255), 
                           config.current_brightness)
            else:
                # Paint gap LED black.
                strip.set_pixel(led, math.floor(enums.colourDi[enums.WColour.White][0]*255),
                           math.floor(enums.colourDi[enums.WColour.White][1]*255),
                           math.floor(enums.colourDi[enums.WColour.White][2]*255), 
                           config.current_brightness)
                
            local_led_index += 1

    info_string = "Pattern: Fixed Morse. Colour: " + str(current_colour) \
                    + ". Brightness: " + str(config.current_brightness)
    wlogger.log_info(info_string)
    wlogger.log_info(strip.leds)

def all_on(strip, blockList):
    """ This function turns the LEDs in the given blocks on."""
        
    if not blockList:
        return

    current_colour = blockList[0].get_colour()
    
    if print_debug: 
        print("----------------------------")
        print("All On")
        print(current_colour)
        print(config.current_brightness)


    # The index of the LED within the current blocks.
    local_led_index = 0
    
    for block in blockList:
        if block.get_direction():
            ledList = np.arange(block.get_end_index(), block.get_start_index(), -1)
        else:
            ledList = np.arange(block.get_start_index(), block.get_end_index())
            
        for led in ledList:
            
            # Paint single LEDS with given colour
            strip.set_pixel(led, math.floor(enums.colourDi[current_colour][0]*255),
                           math.floor(enums.colourDi[current_colour][1]*255),
                           math.floor(enums.colourDi[current_colour][2]*255),
                           config.current_brightness)


            local_led_index += 1

    info_string = "Pattern: All On. Colour: " + str(current_colour) \
                    + ". Brightness: " + str(config.current_brightness)
    wlogger.log_info(info_string)
    wlogger.log_info(strip.leds)
    
def all_off(strip, blockList):
    """ This function turns all LEDs in the blocks given off."""
        
    if not blockList:
        return

    
    if print_debug: 
        print("----------------------------")
        print("All Off")
        print(config.current_brightness)

    # The index of the LED within the current blocks.
    local_led_index = 0
    
    for block in blockList:
        if block.get_direction():
            ledList = np.arange(block.get_end_index(), block.get_start_index(), -1)
        else:
            ledList = np.arange(block.get_start_index(), block.get_end_index())
            
        for led in ledList:
            
            # Paint LED black.
            strip.set_pixel(led, 0.0, 0.0, 0.0)
            local_led_index += 1

    info_string = "Pattern: All Off."
    wlogger.log_info(info_string)
    wlogger.log_info(strip.leds)

def change_colour_of_on_leds(strip, blockList):
        
    if not blockList:
        return
        
    current_colour = blockList[0].get_colour()
    
    for block in blockList:
        if block.get_direction():
            ledList = np.arange(block.get_end_index(), block.get_start_index(), -1)
        else:
            ledList = np.arange(block.get_start_index(), block.get_end_index())
            
            for led in ledList:
    
                # Only turn LEDs that is already on.
                if strip.is_led_on(led):
                    # Paint led if led "on" in random array.
                    strip.set_pixel(led, math.floor(enums.colourDi[current_colour][0]*255),
                               math.floor(enums.colourDi[current_colour][1]*255),
                               math.floor(enums.colourDi[current_colour][2]*255), 
                               config.current_brightness)

    
def twinkle(strip, num_steps_per_cycle, current_step, current_cycle, blockList):
    """ This function twinkles the LED strip between the indices given"""
        
    if not blockList:
        return
        
    current_colour = blockList[0].get_colour()
    current_speed = blockList[0].get_speed()

    # Update LEDs depending on speed.

    if current_speed == enums.WSpeed.Sloth:
        update_leds = (current_step % 6 == 0)
    elif current_speed == enums.WSpeed.Hare:
        update_leds = (current_step % 3 == 0)
    else: #enums.WSpeed.Cheetah:
        update_leds = (current_step % 1 == 0)
        
    # Return early if we do not need to update the LEDs
    if not update_leds:
        return


    if print_debug: 
        print("----------------------------")
        print("Twinkling")
        print(current_speed)
        print(current_colour)
        print(config.current_brightness)
        
    # Calculate total number of LEDs
    total_num_leds = 0
    for block in blockList:
        block_num_leds = block.get_end_index() - block.get_start_index()
        total_num_leds += block_num_leds
        
    # Calculate random array of 0 and 1s to display.
    twinkle_array = np.random.choice([0, 1], size=(total_num_leds,), p=[3./4, 1./4])
    
    # Calculate random array of 0 and 1s to change.
    change_array = np.random.choice([0, 1], size=(total_num_leds,), p=[1./10, 9./10])
    #change_array = ones.

    # The index of the LED within the current blocks.
    local_led_index = 0
    
    for block in blockList:
        if block.get_direction():
            ledList = np.arange(block.get_end_index(), block.get_start_index(), -1)
        else:
            ledList = np.arange(block.get_start_index(), block.get_end_index())
            
        for led in ledList:

            if change_array[local_led_index] and twinkle_array[local_led_index]:
                # Paint twinkle if led "on"
                strip.set_pixel(led, math.floor(enums.colourDi[current_colour][0]*255),
                           math.floor(enums.colourDi[current_colour][1]*255),
                           math.floor(enums.colourDi[current_colour][2]*255), 
                           config.current_brightness)
            else:
                # Paint gap LED black.
                strip.set_pixel(led, 0.0, 0.0, 0.0)
                
            local_led_index += 1
    

    info_string = "Pattern: Twinkling. Colour: " + str(current_colour) + ". Speed: " \
                  + str(current_speed) + ". Brightness: " + str(config.current_brightness)
    wlogger.log_info(info_string)
    wlogger.log_info(strip.leds)
    

def random_in_out(strip, num_steps_per_cycle, current_step, current_cycle, blockList):
    """ This function randomly fills the LED strip between the indices given and 
    then randomly turns them off"""
        
    if not blockList:
        return
        
    current_colour = blockList[0].get_colour()
    current_speed = blockList[0].get_speed()
    
    # Update Colour
    change_colour_of_on_leds(strip, blockList)

    # Update LEDs depending on speed.

    if current_speed == enums.WSpeed.Sloth:
        num_steps_between_changes = 5
    elif current_speed == enums.WSpeed.Hare:
        num_steps_between_changes = 2
    else: #enums.WSpeed.Cheetah:
        num_steps_between_changes = 1
        
    #Configure
    num_steps_in_pattern = 20
    update_leds = (current_step % num_steps_between_changes == 0)
    
    # Return early if we do not need to update the LEDs
    if not update_leds:
        return

    if print_debug: 
        print("----------------------------")
        print("RandomInOut")
        print(current_speed)
        print(current_colour)
        print(config.current_brightness)
        
    # Calculate total number of LEDs
    total_num_leds = 0
    for block in blockList:
        block_num_leds = block.get_end_index() - block.get_start_index()
        total_num_leds += block_num_leds
        
    
    # Paint all LEDs black.
    if blockList[0].get_pattern_index() == 0:
        ledList = np.arange(block.get_start_index(), block.get_end_index())
            
        for led in ledList:
                # Paint gap LED black.
                strip.set_pixel(led, 0.0, 0.0, 0.0)
                
    # Paint all LEDs coloured. This is toleranced.
    elif abs(blockList[0].get_pattern_index() - 1) < 0.001:
        for block in blockList:
            if block.get_direction():
                ledList = np.arange(block.get_end_index(), block.get_start_index(), -1)
            else:
                ledList = np.arange(block.get_start_index(), block.get_end_index())
                
            for led in range(block.get_start_index(), block.get_end_index()):
                strip.set_pixel(led, math.floor(enums.colourDi[current_colour][0]*255),
                                    math.floor(enums.colourDi[current_colour][1]*255),
                                    math.floor(enums.colourDi[current_colour][2]*255), 
                                    config.current_brightness)
                                    
    elif blockList[0].get_pattern_index() < 1:
        
        filled_proportion = blockList[0].get_pattern_index()/2

        # Calculate random array of 0 and 1s to display.
        random_fill_array = np.random.choice([0, 1], size=(total_num_leds,), p=[(1 - filled_proportion), filled_proportion])


        # The index of the LED within the current blocks.
        local_led_index = 0
        
        for block in blockList:
            for led in range(block.get_start_index(), block.get_end_index()):
    
                # Only turn on LEDs don't turn them off.
                if random_fill_array[local_led_index]:
                    # Paint led if led "on" in random array.
                    strip.set_pixel(led, math.floor(enums.colourDi[current_colour][0]*255),
                               math.floor(enums.colourDi[current_colour][1]*255),
                               math.floor(enums.colourDi[current_colour][2]*255), 
                               config.current_brightness)
                
                local_led_index += 1
                               
    elif blockList[0].get_pattern_index() > 1:
        
        un_filled_proportion = (blockList[0].get_pattern_index() - 1)/2

        # Calculate random array of 0 and 1s to display.
        random_fill_array = np.random.choice([0, 1], size=(total_num_leds,), p=[(un_filled_proportion), (1- un_filled_proportion)])


        # The index of the LED within the current blocks.
        local_led_index = 0
        
        for block in blockList:
            for led in range(block.get_start_index(), block.get_end_index()):
    
                # Only turn off LEDs don't turn them on.
                if not random_fill_array[local_led_index]:
                    # Paint gap LED black.
                    strip.set_pixel(led, 0.0, 0.0, 0.0)
                    
                local_led_index += 1
                

    blockList[0].increment_pattern_index(1/num_steps_in_pattern)
    
    if blockList[0].get_pattern_index() > 2:
        blockList[0].set_pattern_index(0)


    info_string = "Pattern: RandomInOut. Colour: " + str(current_colour) + ". Speed: " \
                  + str(current_speed) + ". Brightness: " + str(config.current_brightness)
    wlogger.log_info(info_string)
    wlogger.log_info(strip.leds)
    
    
def colour_snakes_combine(strip, num_steps_per_cycle, current_step, current_cycle, blockList):
    """ This function sets of snakes of different colours moving in opposite directions
        and combines them where they overlap"""
        
    if not blockList:
        return
        
        
    snake_length = 5
    mid_chain_gap = 10
    chain_gap = 30
    
    snake_chain_length = snake_length*3 + mid_chain_gap*2
    single_colour_cycle_length = snake_chain_length + chain_gap
    full_cycle_length = single_colour_cycle_length*3

        
    current_speed = blockList[0].get_speed()

    if print_debug: 
        print("----------------------------")
        print("ColourSnakesCombine")
        print(current_speed)
        print(config.current_brightness)
        
    # Calculate total number of LEDs
    total_num_leds = 0
    for block in blockList:
        block_num_leds = block.get_end_index() - block.get_start_index()
        total_num_leds += block_num_leds
        
    
    # Pattern specific behaviour
    pattern_speed_factor = 1
    num_steps_per_pattern_step = enums.speedDi[current_speed]*pattern_speed_factor

    # The index of the LED within the current blocks.
    local_led_index = 0
    
    
    # First colour the snakes moving in one direction.
    for block in blockList:
        if block.get_direction():
            ledList = np.arange(block.get_end_index(), block.get_start_index(), -1)
        else:
            ledList = np.arange(block.get_start_index(), block.get_end_index())
            
        for led in ledList:
            
            current_pattern_index = (local_led_index + blockList[0].get_pattern_index()) % full_cycle_length
            
            if current_pattern_index < single_colour_cycle_length:
                current_colour = enums.WColour.Blue
            elif current_pattern_index < 2*single_colour_cycle_length:
                current_colour = enums.WColour.Red
            else:
                current_colour = enums.WColour.Green
            
            sub_pattern_index = current_pattern_index % single_colour_cycle_length
            if  sub_pattern_index < snake_chain_length \
                and sub_pattern_index % (snake_length + mid_chain_gap) < snake_length:
                    
                # Paint snake LEDS with given colour
                strip.set_pixel(led, math.floor(enums.colourDi[current_colour][0]*255),
                           math.floor(enums.colourDi[current_colour][1]*255),
                           math.floor(enums.colourDi[current_colour][2]*255), 
                           config.current_brightness)
            else:
                # Paint gap LED black.
                strip.set_pixel(led, 0.0, 0.0, 0.0)
                
            local_led_index += 1
            
            
    # Add the snakes moving in the other direction.
    for block in blockList:
        
        if block.get_direction():
            ledList = np.arange(block.get_end_index(), block.get_start_index(), -1)
        else:
            ledList = np.arange(block.get_start_index(), block.get_end_index())
            
        for led in ledList:
            
            current_pattern_index = (local_led_index - blockList[0].get_pattern_index()) % full_cycle_length
            
            if current_pattern_index < single_colour_cycle_length:
                current_colour = enums.WColour.Blue
            
            elif current_pattern_index < 2*single_colour_cycle_length:
                current_colour = enums.WColour.Red

            else:
                current_colour = enums.WColour.Green

        
            
            sub_pattern_index = current_pattern_index % single_colour_cycle_length
            if  sub_pattern_index < snake_chain_length \
                and sub_pattern_index % (snake_length + mid_chain_gap) < snake_length:
                    
                # Paint snake LEDS with given colour
                
                red, blue, green = strip.get_pixel(led)
                red = red + (math.floor(enums.colourDi[current_colour][0]*255)) % 256
                blue = blue + (math.floor(enums.colourDi[current_colour][1]*255)) % 256
                green = green + (math.floor(enums.colourDi[current_colour][2]*255)) % 256
                
                strip.set_pixel(led, red, blue, green, config.current_brightness)

            local_led_index += 1
            
    
    if(current_step % num_steps_per_pattern_step == 0):
        blockList[0].increment_pattern_index(1)


    info_string = "Pattern: Colour Snakes Combine. Colour: " + str(current_colour) + ". Speed: " \
                  + str(current_speed) + ". Brightness: " + str(config.current_brightness)
    wlogger.log_info(info_string)
    wlogger.log_info(strip.leds)
    
def bi_colour_snakes_combine(strip, num_steps_per_cycle, current_step, current_cycle, colour_b, blockList):
    """ This function sets of snakes of different colours moving in opposite directions
        and combines them where they overlap"""
        
    if not blockList:
        return
        
        
    snake_length = 10
    mid_chain_gap = 15
    chain_gap = 40
    
    snake_chain_length = snake_length*3 + mid_chain_gap*2
    single_colour_cycle_length = snake_chain_length + chain_gap
    
        
    current_speed = blockList[0].get_speed()

    if print_debug: 
        print("----------------------------")
        print("ColourSnakesCombine")
        print(current_speed)
        print(config.current_brightness)
        
    # Calculate total number of LEDs
    total_num_leds = 0
    for block in blockList:
        block_num_leds = block.get_end_index() - block.get_start_index()
        total_num_leds += block_num_leds
        
    
    # Pattern specific behaviour
    pattern_speed_factor = 1
    num_steps_per_pattern_step = enums.speedDi[current_speed]*pattern_speed_factor

    # The index of the LED within the current blocks.
    local_led_index = 0
    
    
    # First colour the snakes moving in one direction.
    for block in blockList:
        if block.get_direction():
            ledList = np.arange(block.get_end_index(), block.get_start_index(), -1)
        else:
            ledList = np.arange(block.get_start_index(), block.get_end_index())
            
        for led in ledList:
            
            current_pattern_index = (local_led_index + blockList[0].get_pattern_index()) % single_colour_cycle_length
            
            current_colour = block.get_colour()
            

            if  current_pattern_index < snake_chain_length \
                and current_pattern_index % (snake_length + mid_chain_gap) < snake_length:
                    
                # Paint snake LEDS with given colour
                strip.set_pixel(led, math.floor(enums.colourDi[current_colour][0]*255),
                           math.floor(enums.colourDi[current_colour][1]*255),
                           math.floor(enums.colourDi[current_colour][2]*255), 
                           config.current_brightness)
            else:
                # Paint gap LED black.
                strip.set_pixel(led, 0.0, 0.0, 0.0)
                
            local_led_index += 1
            
            
    # Add the snakes moving in the other direction.
    for block in blockList:
        if block.get_direction():
            ledList = np.arange(block.get_end_index(), block.get_start_index(), -1)
        else:
            ledList = np.arange(block.get_start_index(), block.get_end_index())
            
        for led in ledList:
            
            current_pattern_index = (local_led_index - blockList[0].get_pattern_index()) % single_colour_cycle_length
            
            current_colour = colour_b
            
            if  current_pattern_index < snake_chain_length \
                and current_pattern_index % (snake_length + mid_chain_gap) < snake_length:
                    
                # Paint snake LEDS with given colour
                
                red, blue, green = strip.get_pixel(led)
                red = red + (math.floor(enums.colourDi[current_colour][0]*255)) % 256
                blue = blue + (math.floor(enums.colourDi[current_colour][1]*255)) % 256
                green = green + (math.floor(enums.colourDi[current_colour][2]*255)) % 256
                
                strip.set_pixel(led, red, blue, green, config.current_brightness)

            local_led_index += 1
            
    
    if(current_step % num_steps_per_pattern_step == 0):
        blockList[0].increment_pattern_index(1)


    info_string = "Pattern: Colour Snakes Combine. Colour: " + str(current_colour) + ". Speed: " \
                  + str(current_speed) + ". Brightness: " + str(config.current_brightness)
    wlogger.log_info(info_string)
    wlogger.log_info(strip.leds)
