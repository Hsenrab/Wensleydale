import ScriptSetup

import Main.config as config
import Internals.Utils.wlogger as wlogger
import HardwareControl.Eyes.wcontroller as wcontroller
import time

# Set the logger up.
wlogger.setup_loggers(config.log_directory)

myController = wcontroller.Controller()
print("Life Test 2")

while(True):
    wlogger.log_info("Begin Cycle")
    wlogger.log_info("Commencing Extreme Down Movement")
    myController.extreme_down(stepSize=1)
    myController.re_centre(stepSize=1)
    wlogger.log_info("Ended Extreme Down Movement")
    
    wlogger.log_info("Commencing Extreme Left Movement")
    myController.extreme_left(1)
    myController.re_centre(1)
    wlogger.log_info("Ended Extreme Left Movement")
    
    wlogger.log_info("Commencing Extreme Up Movement")
    myController.extreme_up(1)
    myController.re_centre(1)
    wlogger.log_info("Ended Extreme Up Movement")
    
    wlogger.log_info("Commencing Extreme Right Movement")
    myController.extreme_right(1)
    myController.re_centre(1)
    wlogger.log_info("Ended Extreme Right Movement")

    wlogger.log_info("Commencing Cross-Eyed Movement")
    myController.cross_eyes(1)
    wlogger.log_info("Ended Cross-Eyed Movement")
    
    wlogger.log_info("Commencing Eye Roll Movement")
    myController.Eye_Roll()
    myController.Eye_Roll()
    myController.Eye_Roll()
    myController.Eye_Roll()
    myController.re_centre(1)
    wlogger.log_info("Ended Eye Roll Movement")
    
    wlogger.log_info("Commencing Straight To Point Sequence")
    myController.straight_to_point(1, 0, 0)
    myController.straight_to_point(1, 50, 0)
    myController.straight_to_point(1, -30, 40)
    myController.straight_to_point(1, 0, 0)
    wlogger.log_info("Ended Straight To Point Sequence")
    
    wlogger.log_info("Commencing combined sequences")
    myController.Eye_Roll()
    myController.straight_to_point(1, 0, 0)
    myController.cross_eyes(1)
    myController.straight_to_point(1, 40, 40)
    myController.straight_to_point(1, 0, 0)
    myController.Low_Cross_Eyes(1)
    #time.sleep(3)
    myController.straight_to_point(1, 0, 0)
    wlogger.log_info("Ended combined sequence")
