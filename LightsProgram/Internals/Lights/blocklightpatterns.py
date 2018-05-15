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
        #Set up different blocks on the dog.
        # Not on Junior self.LegBackRight(0, 288)
        self.LegBackLeft = Block(0, 20)
        self.LegFrontRight = Block(30, 50)
        # Not on Junior self.LegFrontLeft()
        
        #TODO
        #self.CollarFront = Block()
        #self.Collarback = Block()
        #self.BackLowerRight = Block()
        #self.BackLowerLeft = Block()
        #self.BackUpperRight = Block()
        #self.BackUpperLeft = Block()
        #self.EarLeft = Block()
        #self.EarRight = Block()
        #self.EarLeftFront = Block()
        #self.EarRightFront = Block()
        
        
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
        
            
        # Todo - Add the rest of the blocks in.
        self.set_blocks_to_current_global(  self.LegBackLeft,
                                            self.LegFrontRight)
                                            
        

        self.update_blocks(strip, num_steps_per_cycle, current_step, current_cycle,
                        self.LegBackLeft, self.LegFrontRight)

        return 1 # Always update as globals may have changed the pattern.
    
    
        
        
        
