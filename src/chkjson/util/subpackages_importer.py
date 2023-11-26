"""Load all modules from a given subpackage relative to a parent package.

Use this to enable the factory pattern for dynamic class registration.
"""

import importlib
import pkgutil

_CHKJSON_PACKAGE_NAME = "chkjson"


def import_all_modules_in_subpackage(package_name: str, subpackage_name: str):
    # Get a reference to the subpackage module
    subpackage = importlib.import_module(
        f"{package_name}.{subpackage_name}", package=_CHKJSON_PACKAGE_NAME
    )
    # Use pkgutil to iterate through all modules in the subpackage
    for _, module_name, _ in pkgutil.iter_modules(subpackage.__path__):
        # Dynamically import each module
        importlib.import_module(
            f"{package_name}.{subpackage_name}.{module_name}",
            package=_CHKJSON_PACKAGE_NAME,
        )
