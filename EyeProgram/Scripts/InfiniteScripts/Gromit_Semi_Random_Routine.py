import ScriptSetup

import Main.config as config
import Internals.Utils.wlogger as wlogger
import HardwareControl.Eyes.wcontroller as wcontroller
import time
import random
# Set the logger up.

print("Gromit Routine")
wlogger.setup_loggers(config.log_directory)

myController = wcontroller.Controller()
myController.zero_angles()
myController.straight_to_point(myController.tortoise_step_size, myController.resting)

try:
    
    while(True):
        wlogger.log_info("Begin Cycle")
        myController.straight_to_point(myController.tortoise_step_size, myController.extremeRight)
        time.sleep(random.randint(0, 8))
        myController.straight_to_point(myController.tortoise_step_size, myController.extremeLeft)
        time.sleep(random.randint(0, 8))
        myController.straight_to_point(myController.tortoise_step_size, myController.upLeft)
        time.sleep(random.randint(0, 8))
        myController.straight_to_point(myController.tortoise_step_size, myController.downRight)
        time.sleep(random.randint(0, 8))
        myController.straight_to_point(myController.tortoise_step_size, myController.downLeft)
        time.sleep(random.randint(0, 8))
        myController.straight_to_point(myController.tortoise_step_size, myController.resting)
        time.sleep(random.randint(0, 8))
        myController.straight_to_point(myController.tortoise_step_size, myController.crossEyes)
        time.sleep(random.randint(0, 8))
        myController.straight_to_point(myController.tortoise_step_size, myController.resting)
        time.sleep(random.randint(0, 8))
        myController.Gromit_Eye_Roll()
        time.sleep(random.randint(0, 8))
        
except Exception as e:
    # Just print(e) is cleaner and more likely what you want,
    # but if you insist on printing message specifically whenever possible...
    print(e)
    wlogger.log_error(e)

    raise
