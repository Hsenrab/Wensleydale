import ScriptSetup

import Main.config as config
import Internals.Utils.wlogger as wlogger
import HardwareControl.wcontroller as wcontroller
import time

# Set the logger up.
wlogger.setup_loggers(config.log_directory)

myController = wcontroller.Controller()

stepSize = 1
X = 40
Y = 40

myController.extreme_left(stepSize)
wlogger.log_info("Commencing Straight to Point Movement")
myController.straight_to_point(stepSize, X, Y)
myController.straight_to_point(stepSize, 0, 0)
wlogger.log_info("Ended Straight to Point Movement")


time.sleep(1)
print("Done")
