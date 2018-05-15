import ScriptSetup
import time
import Main.config as config
import Internals.Utils.wlogger as wlogger    
import HardwareControl.Eyes.Physical.weye as weye
import HardwareControl.wcontroller as wcontroller

# Set the logger up.
wlogger.setup_loggers(config.log_directory)

myController = wcontroller.Controller()

wlogger.log_info("Commencing Low Cross Eyes Movement")
for i in range(10):
    myController.Low_Cross_Eyes(.5)
    time.sleep(3)
    myController.re_centre(1)
    time.sleep(3)
    
wlogger.log_info("Ended Low Cross Eyes Movement")


time.sleep(1)
print("Done")
