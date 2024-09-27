import logging
import os
import tempfile

import yaml

from richchk.config.richchk_config import RICHCHK_CONFIG_ENV_VAR
from richchk.util import logger


def test_it_creates_logger_with_default_log_level_if_no_config_specified():
    log = logger.get_logger("test_logger")
    assert log.level == logger._DEFAULT_LOG_LEVEl


def test_it_creates_logger_with_config_log_level():
    with tempfile.NamedTemporaryFile(
        prefix="config", suffix=".yaml"
    ) as temp_config_file:
        configdata = {"logging": {"level": "DEBUG"}}
        with open(temp_config_file.name, "w") as f:
            yaml.dump(configdata, f, default_flow_style=False)
        os.environ[RICHCHK_CONFIG_ENV_VAR] = temp_config_file.name
        log = logger.get_logger("test_logger")
        assert log.level == logging.DEBUG
