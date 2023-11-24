"""Provides absolute paths to CHK files used for unit tests.

"""

from pathlib import Path

_RESOURCES_DIR_PATH = Path.joinpath(
    Path(__file__).resolve().parents[0], Path("resources")
)

DEMON_LORE_YATAPI_TEST_CHK_FILE_PATH: str = (
    Path(Path.joinpath(_RESOURCES_DIR_PATH, "demon_lore_yatapi_test.chk"))
    .absolute()
    .as_posix()
)
