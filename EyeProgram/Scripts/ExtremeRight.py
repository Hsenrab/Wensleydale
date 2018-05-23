import ScriptSetup

import Main.config as config
import Internals.Utils.wlogger as wlogger
import HardwareControl.Eyes.wcontroller as wcontroller
import time

# Set the logger up.
wlogger.setup_loggers(config.log_directory)

myController = wcontroller.Controller()

print("Extreme Right")
wlogger.log_info("Commencing Extreme Right Movement")
myController.extreme_right(1)

#myController.re_centre(1)
wlogger.log_info("Ended Extreme Right Movement")

time.sleep(1)
print("Done")
