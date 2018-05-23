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

for_calibration = False

if for_calibration:
    myController.LeftEye.use_mapping = False
    myController.RightEye.use_mapping = False
    use_calibrate_moves = True
else: # For demonstrating the results of the calibration. Should be the same once the calibrated results 
        # have been put on the weye class.
    myController.LeftEye.use_mapping = True
    myController.RightEye.use_mapping = True
    use_calibrate_moves = False
    

# Centre
# The centre should already have been calibrated.

myController.unsafe_move_to(0, 0) # Uncalibrated Move


time.sleep(5)

# Extreme Left
# Manually change results in here until extreme position looks correct 
if use_calibrate_moves:
    myController.unsafe_move_to(-myController.LeftEye.eye_movement_max_radius, -15)
else:
    myController.unsafe_move_to(-myController.LeftEye.eye_movement_max_radius, 0) # Uncalibrated Move

time.sleep(5)

# Extreme Right
# Manually change results in here until extreme position looks correct 
if use_calibrate_moves:
    myController.unsafe_move_to(myController.LeftEye.eye_movement_max_radius, 0)
else:
    myController.unsafe_move_to(myController.LeftEye.eye_movement_max_radius, 0) # Uncalibrated Move

time.sleep(5)



myController.unsafe_move_to(0, 0) # Uncalibrated Move


time.sleep(5)
# Extreme Up
# Manually change results in here until extreme position looks correct 
if use_calibrate_moves:
    myController.unsafe_move_to(15, myController.LeftEye.eye_movement_max_radius)
else:
    myController.unsafe_move_to(0, myController.LeftEye.eye_movement_max_radius) # Uncalibrated Move

time.sleep(5)

# Extreme Down
# Manually change results in here until extreme position looks correct 
if use_calibrate_moves:
    myController.unsafe_move_to(45 , -myController.LeftEye.eye_movement_max_radius)
else:
    myController.unsafe_move_to(0, -myController.LeftEye.eye_movement_max_radius) # Uncalibrated Move

time.sleep(1)
print("Done")
