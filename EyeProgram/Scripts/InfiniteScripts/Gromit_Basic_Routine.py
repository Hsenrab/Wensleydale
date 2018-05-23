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
stepSize = 1
sleepTime = 6
resting = [20, 0, -20, 0]
centre = [0,0]
myController.straight_to_point(stepSize, resting)

try:
    
    while(True):
        wlogger.log_info("Begin Cycle")
        myController.straight_to_point(stepSize, [60, 0])
        time.sleep(random.randint(2, 8))
        myController.straight_to_point(stepSize, [-60, 0])
        time.sleep(random.randint(2, 8))
        myController.straight_to_point(stepSize, [-48, 48])
        time.sleep(random.randint(2, 8))
        myController.straight_to_point(stepSize, [48, -48])
        time.sleep(random.randint(2, 8))
        myController.straight_to_point(stepSize, [-48, -48])
        time.sleep(random.randint(2, 8))
        myController.straight_to_point(stepSize, resting)
        time.sleep(random.randint(2, 8))
        myController.Low_Cross_Eyes(stepSize)
        time.sleep(random.randint(2, 8))
        myController.straight_to_point(stepSize, resting)
        time.sleep(random.randint(2, 8))
        myController.Straight_Eye_Roll(stepSize)
        myController.straight_to_point(stepSize, resting)
        time.sleep(random.randint(2, 8))
        
except Exception as e:
    # Just print(e) is cleaner and more likely what you want,
    # but if you insist on printing message specifically whenever possible...
    print(e.message)
    wlogger.log_error(e.message)

    raise
