"""
loggers.py

Description:
    Loggers to track code execution.

Author: 
    Joan Pont

Copyright:
    Copyright © 2023, Trifork, All Rights Reserved
"""

import                                 sys
import                                 os
import                                 platform
import                                 re
import logging
from   logging.handlers         import RotatingFileHandler
from   pathlib                  import Path
from   datetime                 import datetime


LOG_LOCATION_ENV_VARIABLE = 'LOGS'
LOGS_PATH = os.getenv(LOG_LOCATION_ENV_VARIABLE)


def custom_time(*args):
    """
    Provides a UTC time in 'tuple' format.  Loggers use this for timestamping
    the records.

    Parameters:
        None

    Returns:
        utc_time : 'named tuple'
            i.e.: time.struct_time(tm_year=2023, tm_mon=4, tm_mday=15, tm_hour=0,
                                tm_min=40, tm_sec=47, tm_wday=0, tm_yday=358,
                                tm_isdst=-1)
    """

    utc_dt = datetime.utcnow()
    return utc_dt.timetuple()
    

def custom_logger(f):
    """
    Create a custom logger.
    """

    filename = (f).split('/')
    filename = filename[-1]
    filename = re.sub(r'\.py$', '', filename)
    logger = logging.getLogger(filename)

    ## Create and configure the file logger ###########################
    lfile_handler = None

    if LOGS_PATH:

        if not Path(os.fspath(LOGS_PATH)).exists():
            Path(os.fspath(LOGS_PATH)).mkdir()

        hostname = platform.uname()[1]
        Path(os.fspath(LOGS_PATH) + '/' + hostname).mkdir(exist_ok=True)
        lfile_handler = RotatingFileHandler(
            os.fspath(LOGS_PATH) + '/' + hostname + '/' + filename + '.log',
            maxBytes=100 * 1024 * 1024, backupCount=10
        )
        
        lfile_handler.setLevel(logging.DEBUG)

        # Create formatter and add it to handler
        lfile_format = logging.Formatter(
            fmt='%(asctime)s @ %(levelname)s @ %(name)s @ '\
                '%(funcName)s - %(message)s',
            datefmt='%Y-%m-%dT%H:%M:%SZ'
        )
        lfile_format.converter = custom_time
        lfile_handler.setFormatter(lfile_format)

        # Add handler to the logger
        logger.addHandler(lfile_handler)
    ###################################################################

    ## Create and configure the stdout (screen) logger ################
    lstdout_handler = logging.StreamHandler()

    lstdout_handler.setLevel(logging.INFO)

    # Create formatter and add it to handler
    lstdout_format = logging.Formatter(
        fmt='%(asctime)s @ %(levelname)s @ %(name)s - %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%SZ'
    )
    lstdout_format.converter = custom_time
    lstdout_handler.setFormatter(lstdout_format)

    # Add handler to the logger
    logger.addHandler(lstdout_handler)
    ###################################################################

    # Setting the level of the logging object
    logger.setLevel(logging.DEBUG)

    return logger


# Create a logger to log activity in this module
logger = custom_logger(__file__)