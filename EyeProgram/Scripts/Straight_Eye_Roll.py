import ScriptSetup
import time
import Main.config as config
import Internals.Utils.wlogger as wlogger    
import HardwareControl.Eyes.Physical.weye as weye
import HardwareControl.wcontroller as wcontroller

# Set the logger up.
wlogger.setup_loggers(config.log_directory)

myController = wcontroller.Controller()

wlogger.log_info("Commencing Straight Eye Roll Movement")
for i in range(1):
    myController.Straight_Eye_Roll(1)
    time.sleep(3)
    
wlogger.log_info("Ended Straight Eye Roll Movement")


time.sleep(1)
print("Done")
