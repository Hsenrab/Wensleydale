"""
Contains various configuration variables for the roboplot module.
Attributes:
    wensleydale_directory (str): A convenient reference to the installed location of the wensleydale package on disk.
"""

import os

# File Paths
wensleydale_directory = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__), '..')))
test_data_dir = os.path.normpath(os.path.join(wensleydale_directory, 'Testing', 'Test_Data'))

import Main.enums as enums

# Log Directory
log_directory = os.path.join(wensleydale_directory, 'Logs')


######################
# Hardware set up
######################

# Maximum brightness of LEDs
MAX_BRIGHTNESS = 1

# Delay before button can be pressed again. (Cycles not seconds)
pause_cycles = 30

# Pin set up.
colourInputPin = 24
speedInputPin = 25
patternInputPin = 8

colourOutputPin = 13
speedOutputPin = 16
patternOutputPin = 12

# Number of active leds - this needs to be calibrated once on the dog.
num_active_leds = 204

############################
# Initial configuration on startup
############################

pattern_position_index = 0
wlight_colour = enums.WColour.White
wlight_speed = enums.WSpeed.Cheetah
wlight_pattern = enums.WPattern.Singles
wlight_direction = enums.WDirection.Forwards

patternList = []



