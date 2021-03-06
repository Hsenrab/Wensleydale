#!/usr/bin/env python3
import ScriptSetup

"""Sample script to run a few colour tests on the strip."""
import RPi.GPIO as GPIO
import Internals.Lights.blocklightpatterns as blocklightpatterns
import Internals.Utils.wlogger as wlogger
import Main.config as config
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
        print('Run Block Light Patterns')
        MY_CYCLE = blocklightpatterns.ChangingBlockLightPattern(num_led=NUM_LED, pause_value=0.0, num_steps_per_cycle=120000, num_cycles=1) 
        MY_CYCLE.start()
        
    except KeyboardInterrupt:  # Ctrl-C can halt the light program
        keep_running = False
        wlogger.tear_down_loggers()
        GPIO.cleanup()
        raise KeyboardInterrupt

GPIO.cleanup()
print('Finished the test')
exit()

