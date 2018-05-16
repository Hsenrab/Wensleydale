import ScriptSetup

import Main.config as config
import Internals.Utils.wlogger as wlogger
import HardwareControl.wcontroller as wcontroller

# Set the logger up.
wlogger.setup_loggers(config.log_directory)

myController = wcontroller.Controller()

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
    wlogger.log_info("Ended Eye Roll Movement")
    

