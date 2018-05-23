import ScriptSetup

import Main.config as config
import Internals.Utils.wlogger as wlogger
import HardwareControl.Eyes.wcontroller as wcontroller
import time

# Set the logger up.
wlogger.setup_loggers(config.log_directory)

myController = wcontroller.Controller()

print("Cross-Eyed")
wlogger.log_info("Commencing Cross-Eyed Movement")
myController.cross_eyes(1)
wlogger.log_info("Ended Cross-Eyed Movement")

time.sleep(1)
print("Done")
