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
num_cycles_between_button_recording = 30 #6000


# Pins
touchInputPin = 14
touchOutputPin = 6

BigLEDAOutputPinRed = 17
BigLEDAOutputPinBlue = 27
BigLEDAOutputPinGreen = 22
BigLEDBOutputPinRed = 10
BigLEDBOutputPinBlue = 9
BigLEDBOutputPinGreen = 11
