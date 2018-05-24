import os
import logging
import logging.handlers
import enum

import Internals.Utils.wtime as wtime


def setup_loggers(directory_path, debug_on=False, test_mode_on=False, name='Log', maxBytes=1048576):
    """
    This method sets up the logging method.
    :param directory_path: Directory where the logging files should be stored.
    :param debug_on: If True debug logs are recorded otherwise they are suppressed,
    :param test_mode_on: This stops the times being written into the files for testing.
    :param name: The name of the logger again mainly for testing.
    :param maxBytes: The maximum size of a log file before an new one is created.
    :return:
    """
    if test_mode_on:
        fmt_str = '%(name)s - %(message)s'
    else:
        fmt_str = '%(asctime)s - %(name)s - %(message)s'

    # Set date string so all files from the logger are consistent.
    datestr = wtime.WTime.get_now().strftime("%Y-%m-%d_%H-%M-%S")

    # Set up directory tree.
    info_folder = os.path.join(directory_path, 'Log_Info')
    info_path = os.path.join(info_folder, datestr + "_InfoLog.txt")

    error_folder = os.path.join(directory_path, 'Log_Error')
    error_path = os.path.join(error_folder, datestr + "_ErrorLog.txt")

    debug_folder = os.path.join(directory_path, 'Log_Debug')
    debug_path = os.path.join(debug_folder, datestr + "_DebugLog.txt")

    while os.path.exists(info_path):
        filename, file_extension = os.path.splitext(info_path)
        info_path = filename + 'X.txt'

    # Make folder for info log.
    try:
        os.makedirs(info_folder, exist_ok=True)
    except TypeError:
        try:
            os.makedirs(info_folder, exist_ok=True)
        except OSError:
            if os.path.exists(info_folder):
                pass
            else:
                raise

    # Make folder for warning log.
    try:
        os.makedirs(error_folder, exist_ok=True)
    except TypeError:
        try:
            os.makedirs(error_folder, exist_ok=True)
        except OSError:
            if os.path.exists(error_folder):
                pass
            else:
                raise

    # Make folder for debug log.
    if debug_on:
        try:
            os.makedirs(debug_folder, exist_ok=True)
        except TypeError:
            try:
                os.makedirs(debug_folder, exist_ok=True)
            except OSError:
                if os.path.exists(debug_folder):
                    pass
                else:
                    raise

    # Set format
    formatter = logging.Formatter(fmt_str)

    # Info handler
    info_handler = logging.handlers.RotatingFileHandler(filename=info_path, maxBytes=maxBytes, backupCount=10)
    info_handler.setFormatter(formatter)
    info_handler.setLevel(logging.INFO)

    # Debug handler
    if debug_on:
        debug_handler = logging.handlers.RotatingFileHandler(filename=debug_path,  maxBytes=maxBytes, backupCount=10)
        debug_handler.setFormatter(formatter)
        debug_handler.setLevel(logging.DEBUG)

    # Warning handler
    warning_handler = logging.handlers.RotatingFileHandler(filename=error_path,  maxBytes=maxBytes, backupCount=10000)
    warning_handler.setFormatter(formatter)
    warning_handler.setLevel(logging.WARNING)

    # Set up the logger.
    logger = logging.getLogger(name)

    # Set the message level of the logger. If we want to see debug messages set to debug otherwise set to info.
    if debug_on:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    # Add the handlers to the logger.
    logger.addHandler(info_handler)

    if debug_on:
        logger.addHandler(debug_handler)
    logger.addHandler(warning_handler)

    # Log that the logger was properly initialised.

    if debug_on:
        logger.info('Logger Initialised with Debugging')
    else:
        logger.info('Logger Initialised')


def tear_down_loggers(name='Log'):
    """
    This function removes the loggers handlers.
    :param name: The name of the logger to be torn down.
    :return:
    """
    logger = logging.getLogger(name)

    unclosed_logs = list(logger.handlers)
    for uFile in unclosed_logs:
        logger.removeHandler(uFile)
        uFile.flush()
        uFile.close()



def log_info(message, name='Log'):
    logger = logging.getLogger(name)
    logger.info(message)


def log_debug(message, name='Log'):
    logger = logging.getLogger(name)
    logger.debug(message)


def log_warning(message, name='Log'):
    logger = logging.getLogger(name)
    logger.warning(message)


def log_error(message, name='Log'):
    logger = logging.getLogger(name)
    logger.error(message)