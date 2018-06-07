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
        for i in range(random.randint(3, 8)):
            speed = myController.speeds[random.randint(0,4)]
            position = myController.positions[random.randint(0,9)]
            
            wlogger.log_info("beginning move: " + str(position) + " at speed: " + str(speed))
            
            myController.straight_to_point(speed, position)
            myController.randomSleep()
            
        wlogger.log_info("beginning eye roll")
        myController.Gromit_Eye_Roll()
        myController.randomSleep()
        
except Exception as e:
    # Just print(e) is cleaner and more likely what you want,
    # but if you insist on printing message specifically whenever possible...
    print(e)
    wlogger.log_info(e)

    raise
