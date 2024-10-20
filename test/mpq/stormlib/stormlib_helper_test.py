import os
import platform

import pytest

from richchk.mpq.stormlib.stormlib_helper import StormLibHelper

from ...helpers.stormlib_test_helper import run_test_if_supported_os


def _run_test_if_mac_m1() -> bool:
    return (
        platform.system().lower() == "darwin" and platform.machine().lower() == "arm64"
    )


def test_it_create_stormlib_wrapper_from_embedded_dll():
    if run_test_if_supported_os():
        stormlib = StormLibHelper.load_stormlib(path_to_stormlib_dll=None)
        assert os.path.exists(stormlib.stormlib.path_to_stormlib.path_to_stormlib_dll)


@pytest.mark.usefixtures("embedded_stormlib_path")
def test_it_create_stormlib_wrapper_from_provided_dll(
    embedded_stormlib_path,
):
    if embedded_stormlib_path:
        stormlib = StormLibHelper.load_stormlib(
            path_to_stormlib_dll=embedded_stormlib_path
        )
        assert os.path.exists(stormlib.stormlib.path_to_stormlib.path_to_stormlib_dll)
