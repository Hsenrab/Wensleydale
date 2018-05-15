"""
Contains various configuration variables for the roboplot module.
Attributes:
    wensleydale_directory (str): A convenient reference to the installed location of the wensleydale package on disk.
"""

import os

# File Paths
wensleydale_directory = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__), '..')))
test_data_dir = os.path.normpath(os.path.join(wensleydale_directory, 'Testing', 'Test_Data'))


# Environment variables
real_hardware = True #os.environ.get('WENSLEYDALE', '0') != '0'
if real_hardware:
    print("Using real hardware \n")
else:
    print("Using simulated hardware \n")

# Log Directory
log_directory = os.path.join(wensleydale_directory, 'Logs')
