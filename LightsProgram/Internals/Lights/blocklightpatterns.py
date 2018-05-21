import math
import time
import threading
import Internals.Utils.wstoppablethread as wstoppablethread
import HardwareControl.Environment.Physical.wevents as wevents
from Internals.Lights.colourcycletemplate import ColorCycleTemplate
import Internals.Utils.wlogger as wlogger
import Main.enums as enums
import Main.config as config
import Main.morse as morse
import Internals.Lights.patterns as patterns
import Internals.Lights.wblock as wblock

print_debug = False

        


class BlockLightPattern(ColorCycleTemplate):
    """Paints a pattern on the strip. The strip is split into "blocks" 
    that can have different patterns"""
    
    def init(self, strip, num_led):
        #Set up different blocks on the dog. Current number relate to
        # Screen set up..

        self.LegBackLeft = wblock.WBlock(106, 127)
        self.LegFrontRight = wblock.WBlock(133, 144)
        self.CollarFront = wblock.WBlock(170, 195)
        self.CollarBack = wblock.WBlock(200, 219)
        self.BodyLowerRight = wblock.WBlock(0, 18)
        self.BodyLowerLeft = wblock.WBlock(24, 42)
        self.BodyUpperRight = wblock.WBlock(48, 70)
        self.BodyUpperLeft = wblock.WBlock(75, 100)
        self.EarLeft = wblock.WBlock(225, 239)
        self.EarRight = wblock.WBlock(245, 257)
        self.EarFrontLeft = wblock.WBlock(263, 272)
        self.EarFrontRight = wblock.WBlock(278, 288)
        
        # Set up pins
        wevents.set_up_pins() 
        
        
        # Call sub initialiser.
        self.sub_init()

        
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
            patterns.moving_morse(strip, num_steps_per_cycle, current_step, current_cycle, self.morse, *args)
        elif args[0].get_pattern()  == enums.WPattern.RainbowSlide:
            patterns.rainbow_slide(strip, num_steps_per_cycle, current_step, current_cycle, self.slide_speed, *args)
        elif args[0].get_pattern()  == enums.WPattern.Twinkle:
            patterns.twinkle(strip, num_steps_per_cycle, current_step, current_cycle, *args)
        elif args[0].get_pattern()  == enums.WPattern.RandomInOut:
            patterns.random_in_out(strip, num_steps_per_cycle, current_step, current_cycle, *args)
        else:  #(to catch anything dodgy)
            patterns.singles(strip, num_steps_per_cycle, current_step, current_cycle, *args)
        
        
class ChangingBlockLightPattern(BlockLightPattern):
    """Paints a pattern on the strip based on the status of global variables."""
    
    def sub_init(self):
        # Set up pattern list.
        #config.patternList = [  enums.WPattern.RandomInOut]
        config.patternList = [  enums.WPattern.Singles,
                                enums.WPattern.BlockedSlide,
                                enums.WPattern.Snakes,
                                enums.WPattern.RenishawMorse,
                                enums.WPattern.Twinkle]
                                
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
        
        self.morse = morse.renishaw
                        
        # Set up listening thread.
        self.input_thread = wstoppablethread.WStoppableThread(target=wevents.buttonThread)
        self.input_thread.start()

        
    def sub_cleanup(self):
        self.input_thread.stop()
        self.input_thread.join()
        
    def set_morse(self, morse):
        self.morse = morse
        
    
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
                        
    def sub_cleanup(self):
        pass
        
    
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
                        
        
    def sub_cleanup(self):
        pass
    
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
        self.set_blocks(enums.WColour.Orange,
                        enums.WSpeed.Cheetah,
                        enums.WPattern.MorseFixed,
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
                        
        # Renishaw Morse as default.
        self.morse  = morse.renishaw
        
    def sub_cleanup(self):
        pass
                        
        
    def set_morse(morse):
        self.morse = morse
    
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



