"""Change RichChk behavior (logging, StormLib DLL, etc.) by external config.

Example config.yaml:

logging:

level: INFO
"""

# defines a path to a local config.yaml file
# currently the config only supports changing the logging level globally
RICHCHK_CONFIG_ENV_VAR = "io.sethmachine.richchk.config"
