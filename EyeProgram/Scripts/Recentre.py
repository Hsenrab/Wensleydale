import ScriptSetup
import time

import Main.config as config
import Internals.Utils.wlogger as wlogger
import HardwareControl.wcontroller as wcontroller

# Set the logger up.
wlogger.setup_loggers(config.log_directory)

myController = wcontroller.Controller()

wlogger.log_info("Centering")
print("zero_angles")
myController.zero_angles()

print("Done")

