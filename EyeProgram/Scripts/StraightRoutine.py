import ScriptSetup

import Main.config as config
import Internals.Utils.wlogger as wlogger
import HardwareControl.Eyes.wcontroller as wcontroller
import time

# Set the logger up.
wlogger.setup_loggers(config.log_directory)

myController = wcontroller.Controller()

stepSize = 4

coordinates = [
[0,90, 0, 90],
[0,-90, 0, -90],
[0, 0, 0, 0],
[90, 0, 90, 0],
[-90, 0, -90, 0],
[0, 0, 0, 0],
[63,63,63,63],
[-63,-63,-63,-63],
[0, 0, 0, 0],
[-63,63,-63,63],
[63,-63,63,-63],
[0, 0, 0, 0],
[63,63,63,63],
[-63,63,-63,63],
[-63,-63,-63,-63],
[63,-63,63,-63],
[0, 0, 0, 0],
[0,90, 0, 90],
[90, 0, 90, 0],
[0,-90, 0, -90],
[-90, 0, -90, 0]
[0, 0, 0, 0],]

for position in coordinates:
    myController.straight_to_point(stepSize, position)
    time.sleep(2)
    
print("Done")

