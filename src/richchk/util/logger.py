"""Logger wrapper class.

Taken from:
http://stackoverflow.com/questions/11927278/how-to-configure-logging-in-python
"""

import logging
import os
from typing import Optional

import yaml

from richchk.config.richchk_config import RICHCHK_CONFIG_ENV_VAR

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
LOGDIR = os.path.join(SCRIPT_PATH, "logs")
BASE_LOG = os.path.join(LOGDIR, "richchk.log")
_DEFAULT_LOG_LEVEl = logging.INFO


class Logger(object):
    def __init__(
        self,
        name: str,
        log_file: Optional[str] = None,
        log_dir: Optional[str] = None,
        _use_default_log_level: bool = False,
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
        if not _use_default_log_level:
            logger.setLevel(_determine_log_level_or_default())
        else:
            logger.setLevel(logging.INFO)
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
    name: str,
    logfile: str = BASE_LOG,
    logdir: str = LOGDIR,
    _use_default_log_level: bool = False,
) -> logging.Logger:
    """Define absolute paths for logfile and logdir for outside usage!"""
    return Logger(
        name,
        log_file=logfile,
        log_dir=logdir,
        _use_default_log_level=_use_default_log_level,
    ).get()


def _determine_log_level_or_default() -> int:
    """Check for a config file containing the logging level config.

    Specify the config file path via OS environment variable "richchk.config". It should
    be a path to a .yaml file with the following format:

    logging:     level: INFO

    Level can be one of CRITICAL = 50 FATAL = CRITICAL ERROR = 40 WARNING = 30 WARN =
    WARNING INFO = 20 DEBUG = 10 NOTSET = 0

    :return:
    """
    innerlog = get_logger("RichChkLoggingConfig", _use_default_log_level=True)
    maybe_config_file = os.getenv(RICHCHK_CONFIG_ENV_VAR)
    if maybe_config_file and os.path.exists(maybe_config_file):
        # Read config file
        with open(maybe_config_file, "r") as f:
            config = yaml.safe_load(f)
        # Get logging level from config
        log_level = config["logging"]["level"]
        # Convert log level string to logging module level
        logging_level = getattr(logging, log_level.upper(), _DEFAULT_LOG_LEVEl)
        innerlog.debug(
            f"Using non-default log level {log_level} specified in {maybe_config_file}"
        )
        return logging_level
    elif maybe_config_file and not os.path.exists(maybe_config_file):
        innerlog.error(
            f"No logging config file exists at path specified "
            f"by environment variable {RICHCHK_CONFIG_ENV_VAR} ; using default logging level.  "
            f"File {maybe_config_file} does not exist!"
        )
    return _DEFAULT_LOG_LEVEl
