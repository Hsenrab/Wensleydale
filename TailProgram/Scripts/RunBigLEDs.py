import ScriptSetup
import Internals.Utils.wlogger as wlogger
import HardwareControl.wlights as wlights
import Main.config as config

# Set the logger up.
wlogger.setup_loggers(config.log_directory)
wlogger.log_info("Run Big LEDs")

keep_running = True

while keep_running:
    try:
        # Cycle of light pattern
        print('Run Big Light LEDs')
        wlights.control_big_leds()
        
    except KeyboardInterrupt:  # Ctrl-C can halt the light program
        keep_running = False
        GPIO.cleanup()
        raise KeyboardInterrupt
        
        
