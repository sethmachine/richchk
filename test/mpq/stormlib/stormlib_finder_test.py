import os
import platform
from unittest.mock import patch

import pytest

from richchk.mpq.stormlib.stormlib_finder import StormLibFinder

from ...chk_resources import MACOS_STORMLIB_M1


def _run_test_if_mac_m1() -> bool:
    return (
        platform.system().lower() == "darwin" and platform.machine().lower() == "arm64"
    )


def test_it_uses_provided_macos_m1_dll():
    path_to_stormlib = StormLibFinder.find_stormlib(MACOS_STORMLIB_M1)
    assert os.path.exists(path_to_stormlib.path_to_stormlib_dll)
    assert path_to_stormlib.path_to_stormlib_dll == MACOS_STORMLIB_M1


def test_it_throws_if_provided_dll_does_not_exist():
    madeup_dll_path = "my-fake-dll.dylib"
    with pytest.raises(Exception):
        StormLibFinder.find_stormlib(madeup_dll_path)


def test_it_finds_precompiled_windows_dll_if_no_path_provided():
    with patch("platform.system") as mock_platform_system:
        mock_platform_system.return_value = "Windows"
        path_to_stormlib = StormLibFinder.find_stormlib()
        assert os.path.join(path_to_stormlib.path_to_stormlib_dll)
        assert path_to_stormlib.path_to_stormlib_dll.endswith(".dll")


def test_it_finds_precompiled_macos_m1_dll_if_no_path_provided():
    with (
        patch("platform.system") as mock_platform_system,
        patch("platform.machine") as mock_cpu,
    ):
        mock_platform_system.return_value = "Darwin"
        mock_cpu.return_value = "arm64"
        path_to_stormlib = StormLibFinder.find_stormlib()
        assert os.path.join(path_to_stormlib.path_to_stormlib_dll)
        assert path_to_stormlib.path_to_stormlib_dll.endswith("libstorm.9.22.0.dylib")


def test_it_finds_precompiled_macos_intel_dll_if_no_path_provided():
    with (
        patch("platform.system") as mock_platform_system,
        patch("platform.machine") as mock_cpu,
    ):
        mock_platform_system.return_value = "Darwin"
        mock_cpu.return_value = "not arm64"
        path_to_stormlib = StormLibFinder.find_stormlib()
        assert os.path.join(path_to_stormlib.path_to_stormlib_dll)
        assert path_to_stormlib.path_to_stormlib_dll.endswith("libStorm.dylib")


def test_it_finds_precompiled_linux_dll_if_no_path_provided():
    with (
        patch("platform.system") as mock_platform_system,
        patch("platform.machine") as mock_cpu,
    ):
        mock_platform_system.return_value = "Linux"
        mock_cpu.return_value = "x86_64"
        path_to_stormlib = StormLibFinder.find_stormlib()
        assert os.path.join(path_to_stormlib.path_to_stormlib_dll)
        assert path_to_stormlib.path_to_stormlib_dll.endswith("libstorm.so.9.22.0")


def test_it_throws_if_unrecognized_operating_system():
    with (
        patch("platform.system") as mock_platform_system,
        patch("platform.machine") as mock_cpu,
    ):
        mock_platform_system.return_value = "Linux"
        mock_cpu.return_value = "i386"
        with pytest.raises(OSError):
            StormLibFinder.find_stormlib()
