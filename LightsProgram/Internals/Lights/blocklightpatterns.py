import math
import time
import threading
import HardwareControl.Environment.Physical.wevents as wevents
from Internals.Lights.colourcycletemplate import ColorCycleTemplate
import Internals.Utils.wlogger as wlogger
import Main.enums as enums
import Main.config as config
import Internals.Lights.patterns as patterns

print_debug = False


class Block:
    """ Holds information for each sub block of LEDs """
    def __init__(self, start_index, end_index):
        
        self._start_index = start_index
        self._end_index = end_index
        self._colour = enums.WColour.Blue
        self._speed = enums.WSpeed.Hare
        self._pattern = enums.WPattern.Singles
        self._invert_direction = False
        self._pattern_index = 0
        
    def get_start_index(self):
        return self._start_index
        
    def get_end_index(self):
        return self._end_index
        
    def set_variables(self, colour, speed, pattern):
        self._colour = colour
        self._speed = speed
        
        # Update and reset if the pattern changes.
        if self._pattern is not pattern:
            self._pattern = pattern
            self._pattern_index = 0
        
    def set_colour(self, colour):
        self._colour = colour
        
    def get_colour(self):
        return self._colour
    
    def set_speed(self, speed):
        self._speed = speed
        
    def get_speed(self):
        return self._speed
    
    def set_pattern(self, pattern):
        # Update and reset if the pattern changes.
        if self._pattern is not pattern:
            self._pattern = pattern
            self._pattern_index = 0
            
    def get_pattern(self):
        # Update and reset if the pattern changes.
        return self._pattern
        
    def set_pattern_index(self, pattern_index):
        self._pattern_index = pattern_index
        
    def get_pattern_index(self):
        return self._pattern_index

    def invert_direction(self):
        self._invert_direction = True
        
    def dont_invert_direction(self):
        self._invert_direction = False
        
    def increment_pattern_index(self, increment):
        self._pattern_index += increment
        


class BlockLightPattern(ColorCycleTemplate):
    """Paints a pattern on the strip. The strip is split into "blocks" 
    that can have different patterns"""
    
    def init(self, strip, num_led):
        #Set up different blocks on the dog. Current number relate to
        # Screen set up..

        self.LegBackLeft = Block(106, 127)
        self.LegFrontRight = Block(133, 144)
        self.CollarFront = Block(170, 195)
        self.CollarBack = Block(200, 219)
        self.BodyLowerRight = Block(0, 18)
        self.BodyLowerLeft = Block(24, 42)
        self.BodyUpperRight = Block(48, 70)
        self.BodyUpperLeft = Block(75, 100)
        self.EarLeft = Block(225, 239)
        self.EarRight = Block(245, 257)
        self.EarFrontLeft = Block(263, 272)
        self.EarFrontRight = Block(278, 288)
        
        # Set up pins
        wevents.set_up_pins() 
        
        
        # Call sub initialiser.
        self.sub_init()


        # Set up listening thread.
        input_thread = threading.Thread(target=wevents.buttonThread).start()
        
        
    def set_blocks_to_current_global(self, *args):
        
        with threading.Lock():
            current_pattern = config.wlight_pattern
            current_speed = config.wlight_speed
            current_colour = config.wlight_colour

        
        for block in args:
            block.set_variables(current_colour, current_speed, current_pattern)
            

    def set_blocks(self, colour, speed, pattern, *args):
        for block in args:
            block.set_variables(colour, speed, pattern)
            
            
        
    def update_blocks(self, strip, num_steps_per_cycle, current_step, current_cycle,*args):
        if not args:
            return

        # Assume all blocks have the same local pattern/colour/speed
        
        if args[0].get_pattern() == enums.WPattern.Singles:
            patterns.singles(strip, num_steps_per_cycle, current_step, current_cycle, *args)
        elif args[0].get_pattern()  == enums.WPattern.AllOn:
            patterns.all_on(strip, *args)
        elif args[0].get_pattern()  == enums.WPattern.Slide:
            patterns.slide(strip, num_steps_per_cycle, current_step, current_cycle, self.slide_speed, *args)
        elif args[0].get_pattern()  == enums.WPattern.BlockedSlide:
            for block in args:
                patterns.slide(strip, num_steps_per_cycle, current_step, current_cycle, self.slide_speed, block)
        elif args[0].get_pattern()  == enums.WPattern.Snakes:
            patterns.snakes(strip, num_steps_per_cycle, current_step, current_cycle, *args)
        elif args[0].get_pattern()  == enums.WPattern.RenishawMorse:
            patterns.renishaw(strip, num_steps_per_cycle, current_step, current_cycle, *args)
        elif args[0].get_pattern()  == enums.WPattern.RainbowSlide:
            patterns.rainbow_slide(strip, num_steps_per_cycle, current_step, current_cycle, self.slide_speed, *args)
        else:  #(to catch anything dodgy)
            patterns.singles(strip, num_steps_per_cycle, current_step, current_cycle, *args)
        
        
class ChangingBlockLightPattern(BlockLightPattern):
    """Paints a pattern on the strip based on the status of global variables."""
    
    def sub_init(self):
        # Set up pattern list.
        config.patternList = [enums.WPattern.BlockedSlide]
        #config.patternList = [  enums.WPattern.Singles,
                                #enums.WPattern.BlockedSlide,
                                #enums.WPattern.Snakes,
                                #enums.WPattern.RenishawMorse]
                                
        # Set up colour list.
        config.colourList = [   enums.WColour.Orange,
                                enums.WColour.Red,
                                enums.WColour.Pink,
                                enums.WColour.Blue,
                                enums.WColour.Cyan,
                                enums.WColour.Green,
                                enums.WColour.Yellow]
                                
        # Set up speed list.
        config.speedList = [   enums.WSpeed.Sloth,
                                enums.WSpeed.Hare,
                                enums.WSpeed.Cheetah]
                                
                                
        # Calibrate on dog.
        self.slide_speed = 10
        
    
    def update(self, strip, num_led, num_steps_per_cycle, current_step,
               current_cycle):    
            
        self.set_blocks_to_current_global(  self.LegBackLeft, 
                                            self.LegFrontRight,
                                            self.BodyUpperLeft,
                                            self.BodyUpperRight,
                                            self.BodyLowerLeft,
                                            self.BodyLowerRight,
                                            self.CollarFront,
                                            self.CollarBack,
                                            self.EarLeft,
                                            self.EarRight,
                                            self.EarFrontLeft,
                                            self.EarFrontRight)
                                                                
        

        self.update_blocks(strip, num_steps_per_cycle, current_step, current_cycle,
                        self.BodyLowerRight,
                        self.BodyLowerLeft,
                        self.BodyUpperRight,
                        self.BodyUpperLeft,
                        self.LegBackLeft, 
                        self.LegFrontRight,
                        self.CollarFront,
                        self.CollarBack,
                        self.EarLeft,
                        self.EarRight,
                        self.EarFrontLeft,
                        self.EarFrontRight)

        return 1 # Always update as globals may have changed the pattern.
        
class AllWhitePattern(BlockLightPattern):
    """Paints a pattern on the strip based on the status of global variables."""
    
    def sub_init(self):
        #Set block pattern.
        self.set_blocks(enums.WColour.White,
                        enums.WSpeed.Sloth,
                        enums.WPattern.AllOn,
                        self.LegBackLeft, 
                        self.LegFrontRight,
                        self.BodyUpperLeft,
                        self.BodyUpperRight,
                        self.BodyLowerLeft,
                        self.BodyLowerRight,
                        self.CollarFront,
                        self.CollarBack,
                        self.EarLeft,
                        self.EarRight,
                        self.EarFrontLeft,
                        self.EarFrontRight)
        
    
    def update(self, strip, num_led, num_steps_per_cycle, current_step,
               current_cycle):    

        self.update_blocks(strip, num_steps_per_cycle, current_step, current_cycle,
                        self.BodyLowerRight,
                        self.BodyLowerLeft,
                        self.BodyUpperRight,
                        self.BodyUpperLeft,
                        self.LegBackLeft, 
                        self.LegFrontRight,
                        self.CollarFront,
                        self.CollarBack,
                        self.EarLeft,
                        self.EarRight,
                        self.EarFrontLeft,
                        self.EarFrontRight)

        return 1 # Always update as globals may have changed the pattern.


class RainbowSlidePattern(BlockLightPattern):
    """Paints a pattern on the strip based on the status of global variables."""
    
    def sub_init(self):
        #Set block pattern.
        self.set_blocks(enums.WColour.White,
                        enums.WSpeed.Cheetah,
                        enums.WPattern.RainbowSlide,
                        self.LegBackLeft, 
                        self.LegFrontRight,
                        self.BodyUpperLeft,
                        self.BodyUpperRight,
                        self.BodyLowerLeft,
                        self.BodyLowerRight,
                        self.CollarFront,
                        self.CollarBack,
                        self.EarLeft,
                        self.EarRight,
                        self.EarFrontLeft,
                        self.EarFrontRight)
                        
        # Calibrate on dog.
        self.slide_speed = 100
                        
        
        
    
    def update(self, strip, num_led, num_steps_per_cycle, current_step,
               current_cycle):    

        self.update_blocks(strip, num_steps_per_cycle, current_step, current_cycle,
                        self.BodyLowerRight,
                        self.BodyLowerLeft,
                        self.BodyUpperRight,
                        self.BodyUpperLeft,
                        self.LegBackLeft, 
                        self.LegFrontRight,
                        self.CollarFront,
                        self.CollarBack,
                        self.EarLeft,
                        self.EarRight,
                        self.EarFrontLeft,
                        self.EarFrontRight)

        return 1 # Always update as globals may have changed the pattern.
        
        
class StationaryMorsePattern(BlockLightPattern):
    """Paints a pattern on the strip based on the status of global variables."""
    
    def sub_init(self):
        #Set block pattern.
        self.set_blocks(enums.WColour.White,
                        enums.WSpeed.Cheetah,
                        enums.WPattern.RainbowSlide,
                        self.LegBackLeft, 
                        self.LegFrontRight,
                        self.BodyUpperLeft,
                        self.BodyUpperRight,
                        self.BodyLowerLeft,
                        self.BodyLowerRight,
                        self.CollarFront,
                        self.CollarBack,
                        self.EarLeft,
                        self.EarRight,
                        self.EarFrontLeft,
                        self.EarFrontRight)
                        
        # Calibrate on dog.
        self.slide_speed = 100
                        
        
        
    
    def update(self, strip, num_led, num_steps_per_cycle, current_step,
               current_cycle):    

        self.update_blocks(strip, num_steps_per_cycle, current_step, current_cycle,
                        self.BodyLowerRight,
                        self.BodyLowerLeft,
                        self.BodyUpperRight,
                        self.BodyUpperLeft,
                        self.LegBackLeft, 
                        self.LegFrontRight,
                        self.CollarFront,
                        self.CollarBack,
                        self.EarLeft,
                        self.EarRight,
                        self.EarFrontLeft,
                        self.EarFrontRight)

        return 1 # Always update as globals may have changed the pattern.



