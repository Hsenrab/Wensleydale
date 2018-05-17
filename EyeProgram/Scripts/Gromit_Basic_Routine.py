import ScriptSetup

import Main.config as config
import Internals.Utils.wlogger as wlogger
import HardwareControl.wcontroller as wcontroller
import time
   
# Set the logger up.
wlogger.setup_loggers(config.log_directory)

myController = wcontroller.Controller()
stepSize = 1
centre = [0,0]
while(True):
    wlogger.log_info("Begin Cycle")
    myController.straight_to_point(stepSize, [60, 0])
    time.sleep(2)
    myController.straight_to_point(stepSize, [-60, 0])
    time.sleep(2)
    myController.straight_to_point(stepSize, [-48, 48])
    time.sleep(2)
    myController.straight_to_point(stepSize, [48, -48])
    time.sleep(2)
    myController.straight_to_point(stepSize, [-48, -48])
    time.sleep(2)
    myController.straight_to_point(stepSize, centre)
    time.sleep(2)
    myController.Low_Cross_Eyes(stepSize)
    time.sleep(2)
    myController.straight_to_point(stepSize, centre)
    time.sleep(2)
    myController.Eye_Roll()
    myController.straight_to_point(stepSize, centre)
    time.sleep(2)

