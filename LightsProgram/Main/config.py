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


import threading

######################
# Hardware set up
######################

lock = threading.Lock()

# Maximum brightness of LEDs
MAX_BRIGHTNESS = 10
global_brightness = 10
NIGHT_BRIGHTNESS = 1 # 1 eventually
current_brightness = MAX_BRIGHTNESS
cycles_without_button_press = 0

# There are approx 9.5 cycles per second.
num_cycles_before_dimming = 300000
num_cycles_before_random_changes = 300
random_change_frequency = 200
num_cycles_between_button_recording = 6000

# Delay before button can be pressed again. (Cycles not seconds)
# There are approx 9.5 cycles per second.
pause_cycles = 25

# Pin set up.
colourInputPin = 24
speedInputPin = 25
patternInputPin = 8

colourOutputPin = 14
speedOutputPin = 15
patternOutputPin = 18

# Number of active leds - this needs to be calibrated once on the dog.
num_active_leds = 204

############################
# Initial configuration on startup
############################

wcolour_index = 0
wspeed_index = 0
wpattern_index = 0

patternList = []
colourList = []
speedList = []




