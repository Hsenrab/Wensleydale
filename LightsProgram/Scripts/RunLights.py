#!/usr/bin/env python3
import ScriptSetup

"""Sample script to run a few colour tests on the strip."""
import RPi.GPIO as GPIO
import Internals.Lights.blocklightpatterns as blocklightpatterns
import Internals.Utils.wlogger as wlogger
import Main.config as config
import Main.morse as morse
import Main.enums as enums
import HardwareControl.Environment.Physical.wevents as wevents
import Internals.Lights.partslidepatterns as partslidepatterns

# Set the logger up.
wlogger.setup_loggers(config.log_directory)
wlogger.log_info("Run Full Pattern")
NUM_LED = 12*144
print("Num LEDS")
print(NUM_LED)

keep_running = True
while keep_running:
    try:
        # Cycle of light pattern
        print('Run Block Light Patterns')
        MY_CYCLE = blocklightpatterns.ChangingBlockLightPattern(num_led=NUM_LED, pause_value=0.0, num_steps_per_cycle=1700, num_cycles=1) 
        MY_CYCLE.start()
        
        print('Run Gromit Colours')
        MY_CYCLE = blocklightpatterns.GromitColours(num_led=NUM_LED, pause_value=3, num_steps_per_cycle=1, num_cycles=1) 
        MY_CYCLE.start()
        
        print('Run GromitSlide')
        MY_CYCLE = partslidepatterns.GromitSlide(num_led=NUM_LED, pause_value=0.0, num_steps_per_cycle=90, num_cycles=0, speed=enums.WSpeed.Cheetah, slide_speed=30)
        MY_CYCLE.start()
        
        print('Run MorseCode')
        MY_CYCLE = blocklightpatterns.FixedMorse(num_led=NUM_LED, pause_value=10, num_steps_per_cycle=1, num_cycles=1, morse=morse.renishaw)
        MY_CYCLE.start()

    
        
    except KeyboardInterrupt:  # Ctrl-C can halt the light program
        keep_running = False
        GPIO.cleanup()
        raise KeyboardInterrupt

GPIO.cleanup()
print('Finished the test')
exit()

