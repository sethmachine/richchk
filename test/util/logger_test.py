import logging
import os

import yaml

from richchk.config.richchk_config import RICHCHK_CONFIG_ENV_VAR
from richchk.util import logger
from richchk.util.fileutils import CrossPlatformSafeTemporaryNamedFile


def test_it_creates_logger_with_default_log_level_if_no_config_specified():
    log = logger.get_logger("test_logger")
    assert log.level == logger._DEFAULT_LOG_LEVEl


def test_it_creates_logger_with_config_log_level():
    with CrossPlatformSafeTemporaryNamedFile(
        prefix="config", suffix=".yaml"
    ) as temp_config_file:
        configdata = {"logging": {"level": "DEBUG"}}
        with open(temp_config_file, "w") as f:
            yaml.dump(configdata, f, default_flow_style=False)
        os.environ[RICHCHK_CONFIG_ENV_VAR] = temp_config_file
        log = logger.get_logger("test_logger")
        assert log.level == logging.DEBUG


def test_it_uses_default_log_level_if_env_variable_exist_but_config_file_does_not():
    os.environ[RICHCHK_CONFIG_ENV_VAR] = "a-config-file-that-does-not-exist.yaml"
    log = logger.get_logger("test_logger")
    assert log.level == logger._DEFAULT_LOG_LEVEl
