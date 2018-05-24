#!/usr/bin/env python3
import ScriptSetup

"""Sample script to run a few colour tests on the strip."""
import RPi.GPIO as GPIO
import Internals.Lights.lightpatterns as lightpatterns
import Internals.Utils.wlogger as wlogger
import Main.config as config
import HardwareControl.wlights as wlights
import Internals.Lights.colourschemes as colorschemes

# Set the logger up.
wlogger.setup_loggers(config.log_directory)
wlogger.log_info("Run Light Patterns")


NUM_LED = 12*144
print("Num LEDS")
print(NUM_LED)

keep_running = True
while keep_running:
    try:
        # Cycle of light pattern
        print('Run Big LED Lights')
        
        
    except KeyboardInterrupt:  # Ctrl-C can halt the light program
        keep_running = False
        GPIO.cleanup()
        raise KeyboardInterrupt
        

GPIO.cleanup()
print('Finished the test')
exit()
