import ScriptSetup

import Main.config as config
import Internals.Utils.wlogger as wlogger
import HardwareControl.wcontroller as wcontroller
import time

# Set the logger up.
wlogger.setup_loggers(config.log_directory)

myController = wcontroller.Controller()

wlogger.log_info("Commencing Extreme Left Movement")
myController.extreme_left(1)
#myController.re_centre(1)
wlogger.log_info("Ended Extreme Left Movement")


time.sleep(1)
print("Done")
