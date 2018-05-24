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
import Internals.Lights.blocklightpatterns as blocklightpatterns

print_debug = False


class PartSlide(blocklightpatterns.BlockLightPattern):
    def __init__(self, num_led, pause_value=0, num_steps_per_cycle=100,
                 num_cycles=-1, global_brightness=255, order='rbg',
                 colour=enums.WColour.White, speed=enums.WSpeed.Hare,
                 slide_speed=100):
        
        super(PartSlide, self).__init__(num_led,
                                        pause_value=pause_value,
                                        num_steps_per_cycle=num_steps_per_cycle,
                                        num_cycles=num_cycles,
                                        global_brightness=global_brightness,
                                        order=order)
                                            
        self.slide_speed = slide_speed
        self.colour = colour
        self.speed = speed
        
    
    def init(self, strip, num_led):
        
        raise NotImplementedError("Please implement the init() method")

                        
    def update(self, strip, num_led, num_steps_per_cycle, current_step,
               current_cycle):    
                   
            raise NotImplementedError("Please implement the update() method")
        
    def sub_cleanup(self):
        pass
        
        
class EarSlide(PartSlide):

    def init(self, strip, num_led):
        
        super(PartSlide, self).init(strip, num_led)

        #Set most of the dog to off.
        self.set_blocks(self.colour,
                        self.speed, # will be ignored
                        enums.WPattern.AllOff,
                        self.BodyLowerRight,
                        self.BodyLowerLeft,
                        self.BodyUpperRight,
                        self.BodyUpperLeft,
                        self.LegBackLeft, 
                        self.LegFrontRight,
                        self.CollarFront,
                        self.CollarBack)
                        
        # Set ears to slide
        self.set_blocks(self.colour,
                        self.speed,
                        enums.WPattern.BlockedSlide,
                        self.EarLeft,
                        self.EarRight,
                        self.EarFrontLeft,
                        self.EarFrontRight)
                        
    def update(self, strip, num_led, num_steps_per_cycle, current_step,
               current_cycle):    

        
        #Set most of the dog to off on first update.
        if current_step == 0:
            self.update_blocks(strip, num_steps_per_cycle, current_step, current_cycle,
                                self.BodyLowerRight,
                                self.BodyLowerLeft,
                                self.BodyUpperRight,
                                self.BodyUpperLeft,
                                self.LegBackLeft, 
                                self.LegFrontRight,
                                self.CollarFront,
                                self.CollarBack)
                    
        self.update_blocks(strip, num_steps_per_cycle, current_step, current_cycle,
                            self.EarLeft,
                            self.EarRight,
                            self.EarFrontLeft,
                            self.EarFrontRight)

        return 1
        
        
class BackSlide(PartSlide):

    def init(self, strip, num_led):
        
        super(PartSlide, self).init(strip, num_led)

        #Set most of the dog to off.
        self.set_blocks(self.colour,
                        self.speed, # will be ignored
                        enums.WPattern.AllOff,
                        self.EarLeft,
                        self.EarRight,
                        self.EarFrontLeft,
                        self.EarFrontRight,
                        self.LegBackLeft, 
                        self.LegFrontRight,
                        self.CollarFront,
                        self.CollarBack)
                        
        # Set body to slide
        self.set_blocks(self.colour,
                        self.speed,
                        enums.WPattern.BlockedSlide,
                        self.BodyLowerRight,
                        self.BodyLowerLeft,
                        self.BodyUpperRight,
                        self.BodyUpperLeft)
                        
    def update(self, strip, num_led, num_steps_per_cycle, current_step,
               current_cycle):    
                   
        #Set most of the dog to off on first update.
        if current_step == 0:
            print(current_step)
            self.update_blocks(strip, num_steps_per_cycle, current_step, current_cycle,
                                self.EarLeft,
                                self.EarRight,
                                self.EarFrontLeft,
                                self.EarFrontRight,
                                self.LegBackLeft, 
                                self.LegFrontRight,
                                self.CollarFront,
                                self.CollarBack)
                    
        self.update_blocks(strip, num_steps_per_cycle, current_step, current_cycle,
                            self.BodyLowerRight,
                            self.BodyLowerLeft,
                            self.BodyUpperRight,
                            self.BodyUpperLeft)

        return 1


class LegSlide(PartSlide):

    def init(self, strip, num_led):
        
        super(PartSlide, self).init(strip, num_led)

        #Set most of the dog to off.
        self.set_blocks(self.colour,
                        self.speed, # will be ignored
                        enums.WPattern.AllOff,
                        self.EarLeft,
                        self.EarRight,
                        self.EarFrontLeft,
                        self.EarFrontRight,
                        self.BodyLowerRight,
                        self.BodyLowerLeft,
                        self.BodyUpperRight,
                        self.BodyUpperLeft,
                        self.CollarFront,
                        self.CollarBack)
                        
        # Set legs to slide
        self.set_blocks(self.colour,
                        self.speed,
                        enums.WPattern.BlockedSlide,
                        self.LegBackLeft, 
                        self.LegFrontRight)
                        
    def update(self, strip, num_led, num_steps_per_cycle, current_step,
               current_cycle):    
                   
        #Set most of the dog to off on first update.
        if current_step == 0:
            self.update_blocks(strip, num_steps_per_cycle, current_step, current_cycle,
                                self.EarLeft,
                                self.EarRight,
                                self.EarFrontLeft,
                                self.EarFrontRight,
                                self.BodyLowerRight,
                                self.BodyLowerLeft,
                                self.BodyUpperRight,
                                self.BodyUpperLeft,
                                self.CollarFront,
                                self.CollarBack)
                    
        self.update_blocks(strip, num_steps_per_cycle, current_step, current_cycle,
                            self.LegBackLeft, 
                            self.LegFrontRight)

        return 1


class GromitSlide(PartSlide):
    
    def init(self, strip, num_led):
        super(PartSlide, self).init(strip, num_led)

        #Set most of the dog to off.
        self.set_blocks(self.colour,
                        self.speed, # will be ignored
                        enums.WPattern.AllOff,
                        self.BodyLowerRight,
                        self.BodyLowerLeft,
                        self.BodyUpperRight,
                        self.BodyUpperLeft,
                        self.LegBackLeft, 
                        self.LegFrontRight,
                        self.CollarFront,
                        self.CollarBack)
                        
        # Set ears to slide
        self.set_blocks(self.colour,
                        self.speed,
                        enums.WPattern.BlockedSlide,
                        self.EarLeft,
                        self.EarRight,
                        self.EarFrontLeft,
                        self.EarFrontRight)
                        
    def update_earslide(self, strip, num_led, num_steps_per_cycle, current_step,
               current_cycle):
                   
        #Set most of the dog to off.
        self.set_blocks(self.colour,
                        self.speed, # will be ignored
                        enums.WPattern.AllOff,
                        self.BodyLowerRight,
                        self.BodyLowerLeft,
                        self.BodyUpperRight,
                        self.BodyUpperLeft,
                        self.LegBackLeft, 
                        self.LegFrontRight,
                        self.CollarFront,
                        self.CollarBack)
                        
        # Set ears to slide
        self.set_blocks(self.colour,
                        self.speed,
                        enums.WPattern.BlockedSlide,
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
                            self.CollarBack)
        
        self.update_blocks(strip, num_steps_per_cycle, current_step, current_cycle,
                            self.EarLeft,
                            self.EarRight,
                            self.EarFrontLeft,
                            self.EarFrontRight)
    
    
    def update_bodyslide_earscollar_on(self, strip, num_led, num_steps_per_cycle, current_step,
                                            current_cycle):
                                                
        #Set ear and collar on.
        self.set_blocks(self.colour,
                        self.speed, # will be ignored
                        enums.WPattern.AllOn,
                        self.EarLeft,
                        self.EarRight,
                        self.EarFrontLeft,
                        self.EarFrontRight,
                        self.CollarFront,
                        self.CollarBack)
                        
        #Set legs off.
        self.set_blocks(self.colour,
                        self.speed, # will be ignored
                        enums.WPattern.AllOff,
                        self.LegBackLeft, 
                        self.LegFrontRight)
                        
        # Set body to slide
        self.set_blocks(self.colour,
                        self.speed,
                        enums.WPattern.BlockedSlide,
                        self.BodyLowerRight,
                        self.BodyLowerLeft,
                        self.BodyUpperRight,
                        self.BodyUpperLeft)
    
        # Update
        self.update_blocks(strip, num_steps_per_cycle, current_step, current_cycle,
                            self.EarLeft,
                            self.EarRight,
                            self.EarFrontLeft,
                            self.EarFrontRight,
                            self.CollarFront,
                            self.CollarBack)
                            
        self.update_blocks(strip, num_steps_per_cycle, current_step, current_cycle,
                            self.LegBackLeft, 
                            self.LegFrontRight)
        
        self.update_blocks(strip, num_steps_per_cycle, current_step, current_cycle,
                            self.BodyLowerRight,
                            self.BodyLowerLeft,
                            self.BodyUpperRight,
                            self.BodyUpperLeft)
    
    
    def update_legslide_earscollarbody_on(self, strip, num_led, num_steps_per_cycle, current_step,
                                        current_cycle):   
    
        #Set ear, collar and body on.
        self.set_blocks(self.colour,
                        self.speed, # will be ignored
                        enums.WPattern.AllOn,
                        self.EarLeft,
                        self.EarRight,
                        self.EarFrontLeft,
                        self.EarFrontRight,
                        self.CollarFront,
                        self.CollarBack,
                        self.BodyLowerRight,
                        self.BodyLowerLeft,
                        self.BodyUpperRight,
                        self.BodyUpperLeft)
                        
        # Set legs to slide
        self.set_blocks(self.colour,
                        self.speed,
                        enums.WPattern.BlockedSlide,
                        self.LegBackLeft, 
                        self.LegFrontRight)
                        
        # Update
        self.update_blocks(strip, num_steps_per_cycle, current_step, current_cycle,
                            self.EarLeft,
                            self.EarRight,
                            self.EarFrontLeft,
                            self.EarFrontRight,
                            self.CollarFront,
                            self.CollarBack,
                            self.BodyLowerRight,
                            self.BodyLowerLeft,
                            self.BodyUpperRight,
                            self.BodyUpperLeft)
        
        self.update_blocks(strip, num_steps_per_cycle, current_step, current_cycle,
                                self.LegBackLeft, 
                                self.LegFrontRight)



    def update(self, strip, num_led, num_steps_per_cycle, current_step, current_cycle):
        
        if current_step < num_steps_per_cycle/3:
            self.update_earslide(strip, num_led, num_steps_per_cycle, current_step,
                                    current_cycle)
                   
        elif current_step < 2*num_steps_per_cycle/3:
            self.update_bodyslide_earscollar_on(strip, num_led, num_steps_per_cycle, current_step,
                                                    current_cycle)
               
        else:
            self.update_legslide_earscollarbody_on(strip, num_led, num_steps_per_cycle, current_step,
                                                    current_cycle)
        return 1
