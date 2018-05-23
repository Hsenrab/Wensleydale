import ScriptSetup

import Main.config as config
import Internals.Utils.wlogger as wlogger
import HardwareControl.Eyes.wcontroller as wcontroller
import time

print("Calibrating")
# Set the logger up.
wlogger.setup_loggers(config.log_directory)

myController = wcontroller.Controller()


# Turn current calibration off before calibrating.
# Do not worry about the path the eyes take to get to the new position.
# Each servo is moving straight to its new position so a straight line between two points is not expected.
myController.LeftEye.use_mapping = False
myController.RightEye.use_mapping = False

# Extreme Left
# Manually change results in here until extreme position looks correct 
# myController.move(-myController.LeftEye.eye_movement_max_radius, 0) # Uncalibrated Move
myController.move_to(-myController.LeftEye.eye_movement_max_radius, 0) 

time.sleep(20)

# Extreme Right
# Manually change results in here until extreme position looks correct 
# myController.move(myController.LeftEye.eye_movement_max_radius, 0) # Uncalibrated Move

myController.move_to(myController.LeftEye.eye_movement_max_radius, -15) 

time.sleep(20)

# Extreme Up
# Manually change results in here until extreme position looks correct 
# myController.move(0, myController.LeftEye.eye_movement_max_radius) # Uncalibrated Move

myController.move_to(0, myController.LeftEye.eye_movement_max_radius)

time.sleep(20)

# Extreme Down
# Manually change results in here until extreme position looks correct 
# myController.move(0, -myController.LeftEye.eye_movement_max_radius) # Uncalibrated Move
myController.move_to(25, -myController.LeftEye.eye_movement_max_radius)

time.sleep(1)
print("Done")
