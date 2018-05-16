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
        
        self.start_index = start_index
        self.end_index = end_index
        self.local_colour = enums.WColour.Blue
        self.local_speed = enums.WSpeed.Hare
        self.local_pattern = enums.WPattern.Singles
        self.invert_direction = False
        
    def set_local_variables(colour, speed, pattern):
        self.local_colour = colour
        self.local_speed = speed
        self.local_pattern = pattern
        
    def set_local_colour(colour):
        self.local_colour = colour
    
    def set_local_speed(speed):
        self.local_speed = speed
    
    def set_local_pattern(pattern):
        self.local_pattern = pattern
        
    def invert_direction():
        self.invert_direction = True
        
    def dont_invert_direction():
        self.invert_direction = False
    

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
        
        # Set up pattern list.
        #config.patternList = [enums.WPattern.Singles, enums.WPattern.Slide,
        #                enums.WPattern.AllOn]
        
        config.patternList = [enums.WPattern.AllOn]
        config.wlight_pattern = config.patternList[0]
        
        # Set up listening thread.
        input_thread = threading.Thread(target=wevents.buttonThread).start()
        
        
    def set_blocks_to_current_global(self, *args):
        
        for block in args:
            block.local_colour = config.wlight_colour
            block.local_speed = config.wlight_speed
            block.local_pattern = config.wlight_pattern

        
    def update_blocks(self, strip, num_steps_per_cycle, current_step, current_cycle,*args):
        if not args:
            return

        # Assume all blocks have the same local pattern/colour/speed
        
        if args[0].local_pattern == enums.WPattern.Singles:
            patterns.singles(strip, num_steps_per_cycle, current_step, current_cycle, *args)
        if args[0].local_pattern == enums.WPattern.AllOn:
            patterns.all_on(strip, *args)
        else: #args[0].local_pattern == config.WPattern.Slide
            patterns.slide(strip, num_steps_per_cycle, current_step, current_cycle, *args)
        
        # pattern runs across all blocks
        
        
class ChangingBlockLightPattern(BlockLightPattern):
    """Paints a pattern on the strip based on the status of global variables."""
    
    def update(self, strip, num_led, num_steps_per_cycle, current_step,
               current_cycle):

        with threading.Lock():
            current_pattern = config.wlight_pattern
            current_speed = config.wlight_speed
            current_colour = config.wlight_colour
    
            
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

        return 1 # Always update as globals may have changed the pattern.
    
    
        
        
        
