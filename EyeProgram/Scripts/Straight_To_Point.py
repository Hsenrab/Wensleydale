import ScriptSetup

import Main.config as config
import Internals.Utils.wlogger as wlogger
import HardwareControl.wcontroller as wcontroller
import time

# Set the logger up.
wlogger.setup_loggers(config.log_directory)

myController = wcontroller.Controller()

stepSize = 1
X = 48
Y = 48


coordinates = [X, Y]
centre = [0, 0]

wlogger.log_info("Commencing Straight to Point Movement")
myController.straight_to_point(stepSize, coordinates)
myController.straight_to_point(stepSize, centre)
wlogger.log_info("Ended Straight to Point Movement")


time.sleep(1)
print("Done")
