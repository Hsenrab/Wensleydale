#!/usr/bin/env python3
import ScriptSetup

"""Sample script to run a few colour tests on the strip."""
import Internals.Lights.interrupt_example_scheme as colorscheme
import Internals.Utils.wlogger as wlogger
import Main.config as config


# Set the logger up.
wlogger.setup_loggers(config.log_directory)
wlogger.log_info("Run Interrupt Example Script")


NUM_LED = 144 + 144 + 144

# Cycle of solid light

MY_CYCLE = colorscheme.SolidInterrupts(num_led=NUM_LED, pause_value=1.0, num_steps_per_cycle=100, num_cycles=1)
MY_CYCLE.start()

print('Finished the test')
