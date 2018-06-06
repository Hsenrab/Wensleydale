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
        
        self.offBlocks = [   self.F_15_06_BodyLowerRight,
                        self.D_13_11_BodyLowerLeft,
                        self.E_14_05_BodyUpperRight,
                        self.C_12_10_BodyUpperLeft,
                        self.I_17_16_LegUpperBack, 
                        self.J_18_17_LegLowerBack,
                        self.G_08_07_LegUpperFront,
                        self.H_09_08_LegLowerFront]
                        
        self.set_blocks(self.colour,
                        self.speed,
                        enums.WPattern.AllOff,
                        self.offBlocks)
                        
                        
        self.slidingBlocks = [self.B_04_03_EarLeft,
                        self.A_01_02_EarRight,
                        self.K_20_20_EarFrontLeft,
                        self.L_19_19_EarFrontRight]
                        
        # Set ears to slide
        self.set_blocks(self.colour,
                        self.speed,
                        enums.WPattern.BlockedSlide,
                        self.slidingBlocks)
                        
    def update(self, strip, num_led, num_steps_per_cycle, current_step,
               current_cycle):    

        
        #Set most of the dog to off on first update.
        if current_step == 0:
            self.update_blocks(strip, num_steps_per_cycle, current_step, current_cycle,
                                self.offBlocks)
                    
        self.update_blocks(strip, num_steps_per_cycle, current_step, current_cycle,
                            self.slidingBlocks)

        return 1
        
        
class BackSlide(PartSlide):

    def init(self, strip, num_led):
        
        super(PartSlide, self).init(strip, num_led)
        
        self.offBlocks = [self.B_04_03_EarLeft,
                        self.A_01_02_EarRight,
                        self.K_20_20_EarFrontLeft,
                        self.L_19_19_EarFrontRight,
                        self.I_17_16_LegUpperBack, 
                        self.J_18_17_LegLowerBack,
                        self.G_08_07_LegUpperFront,
                        self.H_09_08_LegLowerFront]

        #Set most of the dog to off.
        self.set_blocks(self.colour,
                        self.speed, # will be ignored
                        enums.WPattern.AllOff,
                        self.offBlocks)
                        
                        
        self.slideBlocks = [self.F_15_06_BodyLowerRight,
                        self.D_13_11_BodyLowerLeft,
                        self.E_14_05_BodyUpperRight,
                        self.C_12_10_BodyUpperLeft]
        # Set body to slide
        self.set_blocks(self.colour,
                        self.speed,
                        enums.WPattern.BlockedSlide,
                        self.slideBlocks)
                        
    def update(self, strip, num_led, num_steps_per_cycle, current_step,
               current_cycle):    
                   
        #Set most of the dog to off on first update.
        if current_step == 0:
            print(current_step)
            self.update_blocks(strip, num_steps_per_cycle, current_step, current_cycle,
                                self.offBlocks)
                    
        self.update_blocks(strip, num_steps_per_cycle, current_step, current_cycle,
                            self.slideBlocks)

        return 1


class LegSlide(PartSlide):

    def init(self, strip, num_led):
        
        super(PartSlide, self).init(strip, num_led)
        
        self.offBlocks = [self.B_04_03_EarLeft,
                        self.A_01_02_EarRight,
                        self.K_20_20_EarFrontLeft,
                        self.L_19_19_EarFrontRight,
                        self.F_15_06_BodyLowerRight,
                        self.D_13_11_BodyLowerLeft,
                        self.E_14_05_BodyUpperRight,
                        self.C_12_10_BodyUpperLeft]

        #Set most of the dog to off.
        self.set_blocks(self.colour,
                        self.speed, # will be ignored
                        enums.WPattern.AllOff,
                        self.offBlocks)
                        
        # Set legs to slide
        self.set_blocks(self.colour,
                        self.speed,
                        enums.WPattern.Slide,
                        [self.I_17_16_LegUpperBack, 
                        self.J_18_17_LegLowerBack])
                        
        self.set_blocks(self.colour,
                        self.speed,
                        enums.WPattern.Slide,
                        [self.G_08_07_LegUpperFront,
                        self.H_09_08_LegLowerFront])
                        
                        
    def update(self, strip, num_led, num_steps_per_cycle, current_step,
               current_cycle):    
                   
        #Set most of the dog to off on first update.
        if current_step == 0:
            self.update_blocks(strip, num_steps_per_cycle, current_step, current_cycle,
                                self.offBlocks)
                    
        self.slideBlocksA = [self.I_17_16_LegUpperBack, 
                            self.J_18_17_LegLowerBack]
                            
        self.update_blocks(strip, num_steps_per_cycle, current_step, current_cycle,
                            self.slideBlocksA)
                            
                            
        self.slideBlocksB = [self.G_08_07_LegUpperFront,
                            self.H_09_08_LegLowerFront]
                            
        self.update_blocks(strip, num_steps_per_cycle, current_step, current_cycle,
                            self.slideBlocksB)

        return 1
        
        
class GromitBlockSlide(PartSlide):

    def init(self, strip, num_led):
        
        super(PartSlide, self).init(strip, num_led)
        
        self.blockSlideBlocks = [self.B_04_03_EarLeft,
                                self.A_01_02_EarRight,
                                self.K_20_20_EarFrontLeft,
                                self.L_19_19_EarFrontRight,
                                self.F_15_06_BodyLowerRight,
                                self.D_13_11_BodyLowerLeft,
                                self.E_14_05_BodyUpperRight,
                                self.C_12_10_BodyUpperLeft]

        #Set most of the dog to block slide.
        self.set_blocks(self.colour,
                        self.speed, # will be ignored
                        enums.WPattern.BlockSlide,
                        self.blockSlideBlocks)
                        
        # Set legs to slide together
        self.set_blocks(self.colour,
                        self.speed,
                        enums.WPattern.Slide,
                        [self.I_17_16_LegUpperBack, 
                        self.J_18_17_LegLowerBack])
                        
        self.set_blocks(self.colour,
                        self.speed,
                        enums.WPattern.Slide,
                        [self.G_08_07_LegUpperFront,
                        self.H_09_08_LegLowerFront])
                        
                        
    def update(self, strip, num_led, num_steps_per_cycle, current_step,
               current_cycle):    
                   
        #Set most of the dog to off on first update.
        if current_step == 0:
            self.update_blocks(strip, num_steps_per_cycle, current_step, current_cycle,
                                self.blockSlideBlocks)

                            
        self.update_blocks(strip, num_steps_per_cycle, current_step, current_cycle,
                            [self.I_17_16_LegUpperBack, 
                            self.J_18_17_LegLowerBack])
                            
                            
        self.update_blocks(strip, num_steps_per_cycle, current_step, current_cycle,
                            [self.G_08_07_LegUpperFront,
                            self.H_09_08_LegLowerFront])

        return 1


class GromitSlide(PartSlide):
    
    def init(self, strip, num_led):
        super(PartSlide, self).init(strip, num_led)
        
        self.offBlocks = [self.F_15_06_BodyLowerRight,
                        self.D_13_11_BodyLowerLeft,
                        self.E_14_05_BodyUpperRight,
                        self.C_12_10_BodyUpperLeft,
                        self.I_17_16_LegUpperBack, 
                        self.J_18_17_LegLowerBack,
                        self.G_08_07_LegUpperFront,
                        self.H_09_08_LegLowerFront]

        #Set most of the dog to off.
        self.set_blocks(self.colour,
                        self.speed, # will be ignored
                        enums.WPattern.AllOff,
                        self.offBlocks)
                        
        # Set ears to slide
        self.slideBlocks = [self.B_04_03_EarLeft,
                        self.A_01_02_EarRight,
                        self.K_20_20_EarFrontLeft,
                        self.L_19_19_EarFrontRight]
                        
        self.set_blocks(self.colour,
                        self.speed,
                        enums.WPattern.BlockedSlide,
                        self.slideBlocks)
                        
    def update_earslide(self, strip, num_led, num_steps_per_cycle, current_step,
               current_cycle):
                   
        #Set most of the dog to off.
        self.set_blocks(self.colour,
                        self.speed, # will be ignored
                        enums.WPattern.AllOff,
                        self.offBlocks)
                        
        # Set ears to slide
        self.set_blocks(self.colour,
                        self.speed,
                        enums.WPattern.BlockedSlide,
                        self.slideBlocks)
    
        self.update_blocks(strip, num_steps_per_cycle, current_step, current_cycle,
                            self.offBlocks)
        
        self.update_blocks(strip, num_steps_per_cycle, current_step, current_cycle,
                            self.slideBlocks)
    
    
    def update_bodyslide_ears_on(self, strip, num_led, num_steps_per_cycle, current_step,
                                            current_cycle):
                                                
        
        self.onBlocks = [self.B_04_03_EarLeft,
                        self.A_01_02_EarRight,
                        self.K_20_20_EarFrontLeft,
                        self.L_19_19_EarFrontRight]
        #Set ear and on.
        self.set_blocks(self.colour,
                        self.speed, # will be ignored
                        enums.WPattern.AllOn,
                        self.onBlocks)
                        
                        
        self.offBlocks = [self.I_17_16_LegUpperBack, 
                        self.J_18_17_LegLowerBack,
                        self.G_08_07_LegUpperFront,
                        self.H_09_08_LegLowerFront]
        #Set legs off.
        self.set_blocks(self.colour,
                        self.speed, # will be ignored
                        enums.WPattern.AllOff,
                        self.offBlocks)
                        
                        
        self.slideBlocks = [self.F_15_06_BodyLowerRight,
                        self.D_13_11_BodyLowerLeft,
                        self.E_14_05_BodyUpperRight,
                        self.C_12_10_BodyUpperLeft]
                        
        # Set body to slide
        self.set_blocks(self.colour,
                        self.speed,
                        enums.WPattern.BlockedSlide,
                        self.slideBlocks)
    
        # Update
        self.update_blocks(strip, num_steps_per_cycle, current_step, current_cycle,
                            self.offBlocks)
                            
        self.update_blocks(strip, num_steps_per_cycle, current_step, current_cycle,
                            self.onBlocks)
        
        self.update_blocks(strip, num_steps_per_cycle, current_step, current_cycle,
                            self.slideBlocks)
    
    
    def update_legslide_earsbody_on(self, strip, num_led, num_steps_per_cycle, current_step,
                                        current_cycle):   
    
    
        self.onBlocks = [self.B_04_03_EarLeft,
                        self.A_01_02_EarRight,
                        self.K_20_20_EarFrontLeft,
                        self.L_19_19_EarFrontRight,
                        self.F_15_06_BodyLowerRight,
                        self.D_13_11_BodyLowerLeft,
                        self.E_14_05_BodyUpperRight,
                        self.C_12_10_BodyUpperLeft]
        #Set ear and body on.
        self.set_blocks(self.colour,
                        self.speed, # will be ignored
                        enums.WPattern.AllOn,
                        self.onBlocks)
                        
                        
        # Set legs to slide
        self.slideBlocksA = [self.I_17_16_LegUpperBack, 
                            self.J_18_17_LegLowerBack]
                            
        self.set_blocks(self.colour,
                        self.speed,
                        enums.WPattern.Slide,
                        self.slideBlocksA)
                        
        self.slideBlocksB = [self.G_08_07_LegUpperFront,
                            self.H_09_08_LegLowerFront]
                        
        self.set_blocks(self.colour,
                        self.speed,
                        enums.WPattern.Slide,
                        self.slideBlocksB)
                        
        # Update
        self.update_blocks(strip, num_steps_per_cycle, current_step, current_cycle,
                            self.onBlocks)
        
        self.update_blocks(strip, num_steps_per_cycle, current_step, current_cycle,
                                self.slideBlocksA)
                                
        self.update_blocks(strip, num_steps_per_cycle, current_step, current_cycle,
                                self.slideBlocksB)



    def update(self, strip, num_led, num_steps_per_cycle, current_step, current_cycle):
        

        if current_step < num_steps_per_cycle/3:
            self.update_earslide(strip, num_led, num_steps_per_cycle, current_step,
                                    current_cycle)
                   
        elif current_step < 2*num_steps_per_cycle/3:
            self.update_bodyslide_ears_on(strip, num_led, num_steps_per_cycle, current_step,
                                                    current_cycle)
               
        else:
            self.update_legslide_earsbody_on(strip, num_led, num_steps_per_cycle, current_step,
                                                    current_cycle)
        return 1
