
#!/usr/bin/env python3
import ScriptSetup

"""Sample script to run a few colour tests on the strip."""
import RPi.GPIO as GPIO
import Internals.Lights.partslidepatterns as partslidepatterns
import Internals.Utils.wlogger as wlogger
import Main.config as config
import Main.enums as enums
import Main.morse as morse 
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
        # Cycle of bespoke light pattern
        
        print('Run Ear Slide Pattern')
        MY_CYCLE = partslidepatterns.EarSlide(num_led=NUM_LED, pause_value=0.0, num_steps_per_cycle=170, num_cycles=1, speed=enums.WSpeed.Cheetah, slide_speed=170, colour=enums.WColour.Green)
        MY_CYCLE.start()
        
        print('Run Back Slide Pattern')
        MY_CYCLE = partslidepatterns.BackSlide(num_led=NUM_LED, pause_value=0.0, num_steps_per_cycle=170, num_cycles=1, speed=enums.WSpeed.Cheetah, slide_speed=170, colour=enums.WColour.Green)
        MY_CYCLE.start()
        
        print('Run Leg Slide Pattern')
        MY_CYCLE = partslidepatterns.LegSlide(num_led=NUM_LED, pause_value=0.0, num_steps_per_cycle=170, num_cycles=1, speed=enums.WSpeed.Cheetah, slide_speed=170, colour=enums.WColour.Green)
        MY_CYCLE.start()
        
        print('Run GromitSlide')
        MY_CYCLE = partslidepatterns.GromitSlide(num_led=NUM_LED, pause_value=0.0, num_steps_per_cycle=707, num_cycles=1, speed=enums.WSpeed.Cheetah, slide_speed=707, colour=enums.WColour.Green)
        MY_CYCLE.start()
        

    except KeyboardInterrupt:  # Ctrl-C can halt the light program
        keep_running = False
        GPIO.cleanup()
        raise KeyboardInterrupt

GPIO.cleanup()
print('Finished the test')
exit()

