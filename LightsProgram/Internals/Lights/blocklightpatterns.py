import math
import time
import threading
import HardwareControl.Environment.Physical.wevents as wevents
from Internals.Lights.colourcycletemplate import ColorCycleTemplate
import Internals.Utils.wlogger as wlogger

print_debug = False

class Block:
    """ Holds information for each sub block of LEDs """
    def __init__(index_list):
        
        self.index_list = index_list # This should have an even number of elements.
        self.use_local_variables = False
        self.local_colour = WColour.Blue
        self.local_speed = WSpeed.Hare
        self.local_pattern = WPattern.Singles
        self.invert_direction = False
        
    def use_local_variables():
        self.use_local_variables = True
        
    def use_global_varaibles():
        self.use_local_variables = False
        
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
        self.LegBackLeft([0, 288])
        self.LegFrontRight([1440, 170])
        # Not on Junior self.LegFrontLeft()
        
        #TODO
        #self.CollarFront()
        #self.Collarback()
        #self.BackLowerRight()
        #self.BackLowerLeft()
        #self.BackUpperRight()
        #self.BackUpperLeft()
        #self.EarLeft()
        #self.EarRight()
        
        
        
