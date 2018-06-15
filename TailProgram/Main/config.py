"""
Contains various configuration variables for the roboplot module.
Attributes:
    wensleydale_directory (str): A convenient reference to the installed location of the wensleydale package on disk.
"""

import os

# File Paths
wensleydale_directory = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__), '..')))
test_data_dir = os.path.normpath(os.path.join(wensleydale_directory, 'Testing', 'Test_Data'))


# Log Directory
log_directory = os.path.join(wensleydale_directory, 'Logs')


# Button press count
button_press_count = 0


touchInputPin = 15
touchOutputPin = 5


config.num_cycles_before_random_wag = 300
config.random_wag_frequency = 300
config.random_wag_length = 100
