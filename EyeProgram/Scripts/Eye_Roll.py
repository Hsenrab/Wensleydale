import ScriptSetup
import time
import Main.config as config
import Internals.Utils.wlogger as wlogger    
import HardwareControl.Eyes.weye as weye
import HardwareControl.Eyes.wcontroller as wcontroller

# Set the logger up.
wlogger.setup_loggers(config.log_directory)

myController = wcontroller.Controller()


print("EyeRoll")
wlogger.log_info("Commencing Eye Roll Movement")
for i in range(3):
    myController.Eye_Roll()
    
myController.re_centre(1)
wlogger.log_info("Ended Eye Roll Movement")


time.sleep(1)
print("Done")
