import ScriptSetup
import time
import Main.config as config
import Internals.Utils.wlogger as wlogger    
import HardwareControl.Eyes.Physical.weye as weye
import HardwareControl.wcontroller as wcontroller

# Set the logger up.
wlogger.setup_loggers(config.log_directory)

myController = wcontroller.Controller()

wlogger.log_info("Commencing Eye Roll Movement")
for i in range(10):
    myController.Eye_Roll()
    
myController.re_centre(1)
wlogger.log_info("Ended Eye Roll Movement")


time.sleep(1)
print("Done")
