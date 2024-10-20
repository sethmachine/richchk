"""Provides absolute paths to CHK files used for unit tests."""

import os
import re
from pathlib import Path

_RESOURCES_DIR_PATH = Path.joinpath(
    Path(__file__).resolve().parents[0], Path("resources")
)

_CHK_SECTIONS_DIR: Path = Path(
    Path.joinpath(_RESOURCES_DIR_PATH, "transcoders", "test-chk-transcoder-inputs")
).absolute()

_DEMON_LORE_CHK_SECTIONS_DIR: Path = Path(
    Path.joinpath(_RESOURCES_DIR_PATH, "transcoders", "demon-lore-chk-sections")
).absolute()

DEMON_LORE_YATAPI_TEST_CHK_FILE_PATH: str = (
    Path(Path.joinpath(_RESOURCES_DIR_PATH, "demon_lore_yatapi_test.chk"))
    .absolute()
    .as_posix()
)

SCM_CHK_FILE: str = (
    Path(Path.joinpath(_RESOURCES_DIR_PATH, "test-chkjson-scm.chk"))
    .absolute()
    .as_posix()
)

SCX_CHK_FILE: str = (
    Path(Path.joinpath(_RESOURCES_DIR_PATH, "test-chkjson-scx.chk"))
    .absolute()
    .as_posix()
)


def _extract_chk_section_name_from_file_path(file_path: str) -> str:
    section_regex = re.compile(r"(?P<chk_section_name>[^.\\)]+).+")
    maybe_chk_section_name = section_regex.match(os.path.basename(file_path)).group(
        "chk_section_name"
    )
    if maybe_chk_section_name is None:
        raise RuntimeError(f"Invalid CHK section file name: {file_path}")
    return maybe_chk_section_name


CHK_SECTION_FILE_PATHS = {
    _extract_chk_section_name_from_file_path(file_path): Path(
        Path.joinpath(_CHK_SECTIONS_DIR, file_path)
    )
    .absolute()
    .as_posix()
    for file_path in os.listdir(_CHK_SECTIONS_DIR)
}

DEMON_LORE_CHK_SECTION_FILE_PATHS = {
    _extract_chk_section_name_from_file_path(file_path): Path(
        Path.joinpath(_DEMON_LORE_CHK_SECTIONS_DIR, file_path)
    )
    .absolute()
    .as_posix()
    for file_path in os.listdir(_DEMON_LORE_CHK_SECTIONS_DIR)
}

MACOS_STORMLIB_M1 = Path(
    Path.joinpath(_RESOURCES_DIR_PATH, "stormlib/macos/libstorm.9.22.0.dylib")
).absolute()
LINUX_STORMLIB_X86_64 = Path(
    Path.joinpath(_RESOURCES_DIR_PATH, "stormlib/linux/libstorm.so.9.22.0")
).absolute()
WINDOWS_STORMLIB = Path(
    Path.joinpath(_RESOURCES_DIR_PATH, "stormlib/windows/Storm.dll")
).absolute()

EXAMPLE_STARCRAFT_SCX_MAP = Path(
    Path.joinpath(_RESOURCES_DIR_PATH, "stormlib/example-stacraft-map.scx")
).absolute()

EXAMPLE_STARCRAFT_SCM_MAP = Path(
    Path.joinpath(_RESOURCES_DIR_PATH, "stormlib/example-starcraft-map.scm")
).absolute()

COMPLEX_STARCRAFT_SCX_MAP = Path(
    Path.joinpath(_RESOURCES_DIR_PATH, "stormlib/test-chkjson-transcoder.scx")
).absolute()
EXAMPLE_WAV_FILE = Path(
    Path.joinpath(_RESOURCES_DIR_PATH, "stormlib/wavs/monitorhumming5.wav")
).absolute()
