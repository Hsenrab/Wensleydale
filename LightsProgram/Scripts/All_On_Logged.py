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
wlogger.log_info("Run All On Logged")


NUM_LED = 1000
print("Num LEDS")
print(NUM_LED)

keep_running = True
while keep_running:
    
    try:
        print('Run AllOn Pattern')
        MY_CYCLE = blocklightpatterns.GlobalPattern(num_led=NUM_LED, pause_value=1, num_steps_per_cycle=50, num_cycles=1,
                                                    colour=enums.WColour.White, pattern=enums.WPattern.AllOn)
        MY_CYCLE.start()

    except KeyboardInterrupt:  # Ctrl-C can halt the light program
        keep_running = False
        GPIO.cleanup()
        raise KeyboardInterrupt

GPIO.cleanup()
print('Finished the test')
exit()

