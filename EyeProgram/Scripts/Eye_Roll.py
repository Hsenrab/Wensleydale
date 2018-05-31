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
    myController.Gromit_Eye_Roll()
    time.sleep(1)

for i in range(3):
    myController.Gromit_Fast_Eye_Roll()
    time.sleep(1)
print("Done eye roll")
wlogger.log_info("Ended Eye Roll Movement")


time.sleep(1)
print("Done")
