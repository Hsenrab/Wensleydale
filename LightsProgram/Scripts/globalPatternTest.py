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
wlogger.log_info("Run Block Light Pattern")


NUM_LED = 12*144
print("Num LEDS")
print(NUM_LED)

keep_running = True
while keep_running:
    
    try:
        # Cycle of light pattern
        #print('Run Flashing Pattern')
        #MY_CYCLE = blocklightpatterns.GlobalPattern(num_led=NUM_LED, pause_value=0.04, num_steps_per_cycle=200, num_cycles=1) 
        #MY_CYCLE.set_routine(enums.WColour.Blue, enums.WSpeed.Cheetah, enums.WPattern.Flashing)
        #MY_CYCLE.start()
        
        print('Run Snakes Pattern')
        MY_CYCLE = blocklightpatterns.GlobalPattern(num_led=NUM_LED, pause_value=0.04, num_steps_per_cycle=50, num_cycles=1,
                                                    colour=enums.WColour.Blue, speed=enums.WSpeed.Cheetah, pattern=enums.WPattern.Snakes)
        MY_CYCLE.start()
        
        print('Run Singles Pattern')
        MY_CYCLE = blocklightpatterns.GlobalPattern(num_led=NUM_LED, pause_value=0.04, num_steps_per_cycle=50, num_cycles=1,
                                                    colour=enums.WColour.Cyan, speed=enums.WSpeed.Sloth, pattern=enums.WPattern.Singles)
        MY_CYCLE.start()
        
        print('Run Slide Pattern')
        MY_CYCLE = blocklightpatterns.Slide(num_led=NUM_LED, pause_value=0.04, num_steps_per_cycle=200, num_cycles=1,
                                            colour=enums.WColour.Green, speed=enums.WSpeed.Hare, pattern=enums.WPattern.Slide)
        MY_CYCLE.start()
        
        print('Run Rainbow Pattern')
        MY_CYCLE = blocklightpatterns.GlobalPattern(num_led=NUM_LED, pause_value=0.04, num_steps_per_cycle=100, num_cycles=1,
                                                    colour=enums.WColour.Blue, speed=enums.WSpeed.Cheetah, pattern=enums.WPattern.Rainbow)
        MY_CYCLE.start()
        
        print('Run AllOn Pattern')
        MY_CYCLE = blocklightpatterns.GlobalPattern(num_led=NUM_LED, pause_value=0.04, num_steps_per_cycle=50, num_cycles=1,
                                                    colour=enums.WColour.Yellow, pattern=enums.WPattern.AllOn)
        MY_CYCLE.start()
        
        print('Run BlockedSlide Pattern')
        MY_CYCLE = blocklightpatterns.Slide(num_led=NUM_LED, pause_value=0.04, num_steps_per_cycle=100, num_cycles=1,
                                                    colour=enums.WColour.Orange, speed=enums.WSpeed.Cheetah, pattern=enums.WPattern.BlockedSlide)
        MY_CYCLE.start()
        
        print('Run RainbowSlide Pattern')
        MY_CYCLE = blocklightpatterns.Slide(num_led=NUM_LED, pause_value=0.04, num_steps_per_cycle=200, num_cycles=1,
                                                    colour=enums.WColour.Blue, speed=enums.WSpeed.Cheetah, pattern=enums.WPattern.RainbowSlide)
        MY_CYCLE.start()
        
        print('Run Twinkle Pattern')
        MY_CYCLE = blocklightpatterns.GlobalPattern(num_led=NUM_LED, pause_value=0.04, num_steps_per_cycle=100, num_cycles=1,
                                                    colour=enums.WColour.Red, speed=enums.WSpeed.Hare, pattern=enums.WPattern.Twinkle)
        MY_CYCLE.start()
        
        print('Run RandomInOut Pattern')
        MY_CYCLE = blocklightpatterns.GlobalPattern(num_led=NUM_LED, pause_value=0.04, num_steps_per_cycle=200, num_cycles=1,
                                                    colour=enums.WColour.Pink, speed=enums.WSpeed.Sloth, pattern=enums.WPattern.RandomInOut)
        MY_CYCLE.start()
        
        print('Run ColourSnakesCombine Pattern')
        MY_CYCLE = blocklightpatterns.GlobalPattern(num_led=NUM_LED, pause_value=0.04, num_steps_per_cycle=200, num_cycles=1,
                                                    colour=enums.WColour.Blue, speed=enums.WSpeed.Cheetah, pattern=enums.WPattern.ColourSnakesCombine)
        MY_CYCLE.start()
        
        print('Run BiColourSnakesCombine Pattern')
        MY_CYCLE = blocklightpatterns.BiColour(num_led=NUM_LED, pause_value=0.04, num_steps_per_cycle=200, num_cycles=1,
                                                    colour=enums.WColour.Blue, speed=enums.WSpeed.Cheetah, pattern=enums.WPattern.BiColourSnakesCombine)
        MY_CYCLE.start()
        
    except KeyboardInterrupt:  # Ctrl-C can halt the light program
        keep_running = False
        GPIO.cleanup()
        raise KeyboardInterrupt

GPIO.cleanup()
print('Finished the test')
exit()

