#!/usr/bin/env python3
# Add root directory to python path. This needs to be included at the start of every script,
# so that the import all work. However there is a module in the the script folder that can be
# imported.

import os
import sys
import time
currDir = os.path.dirname(os.path.realpath(__file__))
rootDir = os.path.abspath(os.path.join(currDir, '..'))
if rootDir not in sys.path:  # add parent dir to paths
    sys.path.append(rootDir)

import config
import Internals.Utils.wlogger as wlogger
import HardwareControl.Eyes.Virtual.weye as weye
import HardwareControl.wcontroller as wcontroller
import eyepwm





# Set the logger up.
wlogger.setup_loggers(config.log_directory)


try:
    myController = wcontroller.Controller()

    stepSize = 0.02

    # testing extremes
    # myController.extreme_left(stepSize)
    # myController.extreme_right(stepSize)
    # myController.re_centre(stepSize)
    # myController.extreme_up(stepSize)
    # myController.extreme_down(stepSize)
    # myController.re_centre(stepSize)

    # testing combinations
    # myController.extreme_down(stepSize)
    # myController.extreme_left(stepSize)
    # myController.re_centre(stepSize)

    test = myController.LeftEye.x_angle_rad
    test2 = myController.LeftEye.y_angle_rad
    test3 = myController.RightEye.x_angle_rad
    test4 = myController.RightEye.y_angle_rad
    # testing set methods
    # myController.cross_eyes(stepSize)
    myController.Straight_Eye_Roll()
    myController.Straight_Eye_Roll()

    myController.continue_game()

    # while(True):
    #    x=0

    # raise NotImplementedError
    
    # Initialise Eyes

    # Run Eyes
    
except Exception as e:
    # Placeholder
    x = 0

    # Unexpected Exception - all exeptions should be dealt with internally

    # Write exception to log.

    # Deal with exception - at the moment rethrow.

    raise

finally:
    # Placeholder
    x = 0
    
    # Unintialise Eyes
    
    # Log that shut down was activated.
    
    # Shutdown program - Possibly try to "restart program" eventually

    

