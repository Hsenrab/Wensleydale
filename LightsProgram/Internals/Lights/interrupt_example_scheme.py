"""This module contains a few concrete colour cycles to play with"""

from Internals.Lights.colourcycletemplate import ColorCycleTemplate
import Development.ThreadingTest as ThreadingTest
import Internals.Utils.wlogger as wlogger
import threading
import HardwareControl.Environment.Virtual.wevents as wevents

class SolidInterrupts(ColorCycleTemplate):

    def update(self, strip, num_led, num_steps_per_cycle, current_step,
               current_cycle):
        with threading.Lock():
            print(wevents.wlight_colour)
            print(wevents.colourDi[wevents.wlight_colour][0])
            print(wevents.colourDi[wevents.wlight_colour][1])
            print(wevents.colourDi[wevents.wlight_colour][2])
            red = wevents.colourDi[wevents.wlight_colour][0]
            green = wevents.colourDi[wevents.wlight_colour][1]
            blue = wevents.colourDi[wevents.wlight_colour][2]

            x=0

        for led in range(0, num_led):
            # Paint all with given colour
            strip.set_pixel(led, red, green, blue, 5)

        return True




