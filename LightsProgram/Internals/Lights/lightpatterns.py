import math
import time
import threading
import HardwareControl.Environment.Physical.wevents as wevents
from Internals.Lights.colourcycletemplate import ColorCycleTemplate
import Internals.Utils.wlogger as wlogger

print_debug = False

class ChangingLightPattern(ColorCycleTemplate):
    """Paints a pattern on the strip based on the status of global variables."""
    
    def update(self, strip, num_led, num_steps_per_cycle, current_step,
               current_cycle):

        with threading.Lock():
            current_pattern = wevents.wlight_pattern

        if current_pattern == wevents.WPattern.Flashing:
            self.flashing(strip, num_led, num_steps_per_cycle, current_step, current_cycle)
        elif current_pattern == wevents.WPattern.Snakes:
            self.snakes(strip, num_led, num_steps_per_cycle, current_step, current_cycle)
        elif current_pattern == wevents.WPattern.Singles:
            self.singles(strip, num_led, num_steps_per_cycle, current_step, current_cycle)
        elif current_pattern == wevents.WPattern.Rainbow:
            self.rainbow(strip, num_led, num_steps_per_cycle, current_step, current_cycle)
        else:
            x=0

        return 1 # Always update as globals may have changed the pattern.

    def flashing(self, strip, num_led, num_steps_per_cycle, current_step, current_cycle):
        with threading.Lock():
            current_speed = wevents.wlight_speed
            current_colour = wevents.wlight_colour
            current_brightness = wevents.wlight_brightness
        
        if print_debug:
            print("----------------------------")
            print("Flashing")
            print(current_speed)
            print(current_colour)
            print(current_brightness)

        # Pattern specific behaviour
        pattern_speed_factor = 3
        num_steps_per_pattern_step = wevents.speedDi[current_speed]*pattern_speed_factor

        if (current_step % (2*num_steps_per_pattern_step)) < num_steps_per_pattern_step:
            self.lights_on(strip, num_led, current_colour, current_brightness)
        else:
            self.clear_strip(strip)

        info_string = "Pattern: Flashing. Colour: " + str(current_colour) + ". Speed: " \
                      + str(current_speed) + ". Brightness: " + str(current_brightness)
        wlogger.log_info(info_string)
        wlogger.log_info(strip.leds)

    @staticmethod
    def lights_on(strip, num_led, current_colour, current_brightness):
        for led in range(0, num_led):
            # Paint all with given colour
            strip.set_pixel(led, math.floor(wevents.colourDi[current_colour][0]*255),
                           math.floor(wevents.colourDi[current_colour][1]*255),
                           math.floor(wevents.colourDi[current_colour][2]*255),
                            wevents.brightnessDi[current_brightness]/2)

    @staticmethod
    def clear_strip(strip):
        for led in range(strip.num_led):
            strip.set_pixel(led, 0, 0, 0)

    @staticmethod
    def snakes(strip, num_led, num_steps_per_cycle, current_step, current_cycle):
        snake_length = 15
        snake_gap = 30

        with threading.Lock():
            current_speed = wevents.wlight_speed
            current_colour = wevents.wlight_colour
            current_brightness = wevents.wlight_brightness
            
        if print_debug:       
            print("----------------------------")
            print("Snakes")
            print(current_speed)
            print(current_colour)
            print(current_brightness)

        # Pattern specific behaviour
        pattern_speed_factor = 1
        num_steps_per_pattern_step = wevents.speedDi[current_speed]*pattern_speed_factor

        for led in range(0, num_led):

            pattern_step = math.floor(current_step/num_steps_per_pattern_step)

            if (led + pattern_step) % (snake_length + snake_gap) < snake_length:
                # Paint snake LEDS with given colour
                strip.set_pixel(led, math.floor(wevents.colourDi[current_colour][0]*255),
                           math.floor(wevents.colourDi[current_colour][1]*255),
                           math.floor(wevents.colourDi[current_colour][2]*255), wevents.brightnessDi[current_brightness])
            else:
                # Paint gap LED black.
                strip.set_pixel(led, 0.0, 0.0, 0.0)

        info_string = "Pattern: Snakes. Colour: " + str(current_colour) + ". Speed: " \
                      + str(current_speed) + ". Brightness: " + str(current_brightness)
        wlogger.log_info(info_string)
        wlogger.log_info(strip.leds)



    def singles(self, strip, num_led, num_steps_per_cycle, current_step, current_cycle):
        single_gap = 10
        
        with threading.Lock():
            current_speed = wevents.wlight_speed
            current_colour = wevents.wlight_colour
            current_brightness = wevents.wlight_brightness
            
        if print_debug: 
            print("----------------------------")
            print("Singles")
            print(current_speed)
            print(current_colour)
            print(current_brightness)

        # Pattern specific behaviour
        pattern_speed_factor = 1
        num_steps_per_pattern_step = wevents.speedDi[current_speed]*pattern_speed_factor

        for led in range(0, num_led):
            pattern_step = math.floor(current_step/num_steps_per_pattern_step)

            if (led + pattern_step) % (single_gap + 1) == 0:
                # Paint single LEDS with given colour
                strip.set_pixel(led, math.floor(wevents.colourDi[current_colour][0]*255),
                           math.floor(wevents.colourDi[current_colour][1]*255),
                           math.floor(wevents.colourDi[current_colour][2]*255), wevents.brightnessDi[current_brightness])
            else:
                # Paint gap LED black.
                strip.set_pixel(led, 0.0, 0.0, 0.0)

        info_string = "Pattern: Single. Colour: " + str(current_colour) + ". Speed: " \
                      + str(current_speed) + ". Brightness: " + str(current_brightness)
        wlogger.log_info(info_string)
        wlogger.log_info(strip.leds)

    def rainbow(self, strip, num_led, num_steps_per_cycle, current_step, current_cycle):
        
        with threading.Lock():
            current_speed = wevents.wlight_speed
            current_colour = wevents.wlight_colour
            current_brightness = wevents.wlight_brightness
          
        if print_debug:   
            print("----------------------------")
            print("Rainbow")
            print(current_speed)
            print(current_colour)
            print(current_brightness)
        
        
        num_leds_per_gradient = 50 # Index change between two neighboring LEDs
        start_index =  current_step
        
        colour_start, num_wheel_points_per_gradient = ChangingLightPattern.colour_to_wheel_param(current_colour)
        
        for i in range(num_led):
            colour_step = math.floor(num_wheel_points_per_gradient/num_leds_per_gradient)
            
            pattern_index = (start_index + i) % num_leds_per_gradient
            colour_index = math.floor(colour_step*pattern_index)

            if(colour_index < (num_leds_per_gradient/2)):
                wheel_colour = colour_start + colour_index
            else:
                wheel_colour = colour_start + num_leds_per_gradient - colour_index

            # Now rounded and wrapped
            rounded_wheel = int(round(wheel_colour, 0)) % 255
            # Get the actual color out of the wheel
            pixel_color = strip.wheel(rounded_wheel)
            strip.set_pixel_rgb(i, pixel_color, wevents.brightnessDi[current_brightness]/2)
        return 1 # All pixels are set in the buffer, so repaint the strip now
    
    @staticmethod
    def colour_to_wheel_param(colour):
        if(colour == wevents.WColour.Red):
            return 85, 50
        elif(colour == wevents.WColour.Blue):
            return 0, 100
        elif(colour == wevents.WColour.Green):
            return 170, 100
        elif(colour == wevents.WColour.Cyan):
            return 225, 100
        elif(colour == wevents.WColour.Yellow):
            return 100, 60
        elif(colour == wevents.WColour.Pink):
            return 50, 75
        elif(colour == wevents.WColour.Orange):
            return 85, 50
        else: # wevents.WColour.White
            return 0, 1
        
        
        
        
        
        
        
        
