#!/usr/bin/env python3
import ScriptSetup

"""Sample script to run a few colour tests on the strip."""
import RPi.GPIO as GPIO
import Internals.Lights.blocklightpatterns as blocklightpatterns
import Internals.Utils.wlogger as wlogger
import Main.config as config
import Main.enums as enums
import HardwareControl.Environment.Physical.wevents as wevents
import Internals.Lights.colourschemes as colorschemes

# Set the logger up.
wlogger.setup_loggers(config.log_directory)
wlogger.log_info("Run Colour Snakes Combine Pattern")


NUM_LED = 12*144
print("Num LEDS")
print(NUM_LED)

keep_running = True
while keep_running:
    
    try:
        # Cycle of light pattern
        print('Run Colour Snakes Combine Patterns')
        MY_CYCLE = blocklightpatterns.GlobalPattern(num_led=NUM_LED, pause_value=0.04, num_steps_per_cycle=200, num_cycles=1,
                                                    colour=enums.WColour.Blue, speed=enums.WSpeed.Cheetah, pattern=enums.WPattern.ColourSnakesCombine)
        MY_CYCLE.start()
        
        print('Run BiColourSnakesCombine Pattern')
        # No extra variables given
        MY_CYCLE = blocklightpatterns.BiColour(num_led=NUM_LED, pause_value=0.04, num_steps_per_cycle=50, num_cycles=1,
                                                    colour=enums.WColour.Blue, speed=enums.WSpeed.Cheetah, pattern=enums.WPattern.BiColourSnakesCombine)
        MY_CYCLE.start()
        
            
        MY_CYCLE = blocklightpatterns.BiColour(num_led=NUM_LED, pause_value=0.04, num_steps_per_cycle=50, num_cycles=1,
                                                    colour=enums.WColour.Green, speed=enums.WSpeed.Cheetah, pattern=enums.WPattern.BiColourSnakesCombine,
                                                    colour_b=enums.WColour.Pink)
        MY_CYCLE.start()
        
        MY_CYCLE = blocklightpatterns.BiColour(num_led=NUM_LED, pause_value=0.04, num_steps_per_cycle=50, num_cycles=1,
                                                    colour=enums.WColour.White, speed=enums.WSpeed.Cheetah, pattern=enums.WPattern.BiColourSnakesCombine,
                                                    colour_b=enums.WColour.Blue)
        MY_CYCLE.start()
        
        MY_CYCLE = blocklightpatterns.BiColour(num_led=NUM_LED, pause_value=0.04, num_steps_per_cycle=50, num_cycles=1,
                                                    colour=enums.WColour.Green, speed=enums.WSpeed.Cheetah, pattern=enums.WPattern.BiColourSnakesCombine,
                                                    colour_b=enums.WColour.Red)
        MY_CYCLE.start()
        
    except KeyboardInterrupt:  # Ctrl-C can halt the light program
        keep_running = False
        GPIO.cleanup()
        raise KeyboardInterrupt#
        
    keep_running = False

GPIO.cleanup()
print('Finished the test')
exit()

