 #!/usr/bin/env python3
import ScriptSetup
"""Sample script to put all lights on."""
#import HardwareControl.Lights.Virtual.wlight
import Internals.Lights.colourschemes as colorschemes
import Internals.Utils.wlogger as wlogger
NUM_LED = 12*144

# All on as white light - to stop Ctrl C
print('All On')

while True:
  MY_CYCLE = colorschemes.Solid(num_led=NUM_LED, pause_value=1,
                             num_steps_per_cycle=1000, num_cycles=1, global_brightness=50)
                             
  MY_CYCLE.start()

print('Finished the test')
