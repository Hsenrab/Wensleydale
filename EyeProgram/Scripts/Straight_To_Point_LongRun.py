import ScriptSetup

import Main.config as config
import Internals.Utils.wlogger as wlogger
import HardwareControl.wcontroller as wcontroller
import time

# Set the logger up.
wlogger.setup_loggers(config.log_directory)

myController = wcontroller.Controller()

wlogger.log_info("Commencing Straight to Point Movement")
myController.straight_to_point(1, 40, 40)
myController.straight_to_point(1, -40, 40)
myController.straight_to_point(1, 40, 40)
myController.straight_to_point(1, -40, -40)
myController.straight_to_point(1, 40, 40)
myController.straight_to_point(1, 40, -40)
myController.straight_to_point(1, 40, 40)
myController.straight_to_point(1, 0, 0)

myController.straight_to_point(1, -40, 40)
myController.straight_to_point(1, 40, 40)
myController.straight_to_point(1, -40, 40)
myController.straight_to_point(1, 40, -40)
myController.straight_to_point(1, -40, 40)
myController.straight_to_point(1, -40, -40)
myController.straight_to_point(1, -40, 40)
myController.straight_to_point(1, 0, 0)

myController.straight_to_point(1, -40, -40)
myController.straight_to_point(1, 40, -40)
myController.straight_to_point(1, -40, -40)
myController.straight_to_point(1, 40, 40)
myController.straight_to_point(1, -40, -40)
myController.straight_to_point(1, -40, 40)
myController.straight_to_point(1, -40, -40)
myController.straight_to_point(1, 0, 0)

myController.straight_to_point(1, 40, -40)
myController.straight_to_point(1, -40, -40)
myController.straight_to_point(1, 40, -40)
myController.straight_to_point(1, -40, 40)
myController.straight_to_point(1, 40, -40)
myController.straight_to_point(1, 40, 40)
myController.straight_to_point(1, 40, -40)
myController.straight_to_point(1, 0, 0)
wlogger.log_info("Ended Straight to Point Movement")


time.sleep(1)
print("Done")
