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
