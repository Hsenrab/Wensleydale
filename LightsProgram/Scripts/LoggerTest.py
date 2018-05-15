import ScriptSetup
import Main.config as config
import Internals.Utils.wlogger as wlogger


wlogger.setup_logger(config.wensleydale_directory)

wlogger.log_info("Output Message")
