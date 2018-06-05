import ScriptSetup
import Internals.Utils.wlogger as wlogger
import HardwareControl.wtail as wtail
import Main.config as config
import RPi.GPIO as GPIO
from Adafruit_PCA9685 import PCA9685 

# Set the logger up.
wlogger.setup_loggers(config.log_directory)
wlogger.log_info("Run Tail")

keep_running = True

while keep_running:
    try:
        # Cycle of light pattern
        print('Run Tail')
        aTail = wtail.Tail()
        aTail.control_tail()
        
    except KeyboardInterrupt:  # Ctrl-C can halt the light program
        keep_running = False
        print("Cleanup")
        reset = PCA9685(0x41)
        GPIO.cleanup()
        raise KeyboardInterrupt
        
        
