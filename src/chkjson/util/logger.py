"""Logger wrapper class.

Taken from:
http://stackoverflow.com/questions/11927278/how-to-configure-logging-in-python
"""

import logging
import os
from typing import Optional

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
LOGDIR = os.path.join(SCRIPT_PATH, "logs")
BASE_LOG = os.path.join(LOGDIR, "chkjson.log")


class Logger(object):
    def __init__(
        self, name: str, log_file: Optional[str] = None, log_dir: Optional[str] = None
    ):
        assert isinstance(log_dir, str)
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        if not log_file:
            log_file = "{}.log".format(name)
        name = name.replace(".log", "")
        logger = logging.getLogger(
            "%s" % name
        )  # log_namespace can be replaced with your namespace
        logger.setLevel(logging.DEBUG)
        if not logger.handlers:
            file_name = os.path.join(
                log_dir, log_file
            )  # usually I keep the LOGGING_DIR defined in some global settings file
            handler = logging.FileHandler(file_name)
            shandler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s %(levelname)s:%(name)s %(message)s"
            )
            handler.setFormatter(formatter)
            handler.setLevel(logging.DEBUG)
            shandler.setFormatter(formatter)
            shandler.setLevel(logging.DEBUG)
            logger.addHandler(handler)
            logger.addHandler(shandler)
        self._logger = logger

    def get(self) -> logging.Logger:
        return self._logger


def get_logger(
    name: str, logfile: str = BASE_LOG, logdir: str = LOGDIR
) -> logging.Logger:
    """Define absolute paths for logfile and logdir for outside usage!"""
    return Logger(name, log_file=logfile, log_dir=logdir).get()
