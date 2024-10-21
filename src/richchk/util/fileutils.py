"""File system utility functions to simplify file manipulation."""

import os
import re
import tempfile
import typing
from typing import Iterator, Optional


class CrossPlatformSafeTemporaryNamedFile:
    """This custom implementation is needed because of the following limitation of
    tempfile.NamedTemporaryFile:

    > Whether the name can be used to open the file a second time, while the named
    temporary file is still open, > varies across platforms (it can be so used on Unix;
    it cannot on Windows NT or later).

    Taken from:
    https://stackoverflow.com/questions/23212435/permission-denied-to-write-to-my-temporary-file
    """

    def __init__(
        self,
        delete: bool = True,
        prefix: Optional[str] = None,
        suffix: Optional[str] = None,
    ) -> None:
        self._delete = delete
        self._filename = ""
        self._prefix = prefix
        self._suffix = suffix

    def __enter__(self) -> str:
        # Generate a random temporary file name
        self._filename = self._create_filename()
        # Ensure the file is created
        open(self._filename, mode="w").close()
        # Open the file in the given mode
        return self._filename

    def _create_filename(self) -> str:
        parts = []
        if self._prefix:
            parts.append(self._prefix)
        parts.append(os.urandom(24).hex())
        if self._suffix:
            parts.append(self._suffix)
        return os.path.join(tempfile.gettempdir(), "".join(parts))

    def __exit__(
        self, exc_type: typing.Any, exc_val: typing.Any, exc_tb: typing.Any
    ) -> None:
        if self._delete:
            assert isinstance(self._filename, str)
            os.remove(self._filename)


def absolute_filepaths(
    directory: str, depth: int = 0, file_regex: re.Pattern[str] = re.compile(r".+")
) -> Iterator[str]:
    """List all absolute filepaths recursively from a directory.

    :param directory: the directory to begin finding matching files
    :param depth: how many directory levels to explore; a depth of 0 explores only the
        level of the first directory while a depth of -1 recursively explores all
        subdirectories.
    :param file_regex: an optional compiled regular expression; only base file names
        matching the regex are yielded.
    :return: an iterator of absolute filepaths found
    """
    for x in os.listdir(directory):
        path = os.path.join(directory, x)
        if os.path.isfile(path):
            if file_regex.search(path):
                yield path
        elif depth != 0:
            for f in absolute_filepaths(path, depth - 1, file_regex):
                yield f


def absolute_dirpaths(
    directory: str, depth: int = 0, file_pattern: str = r".+"
) -> Iterator[str]:
    """Lists all files joined to directory path.

    Args:     depth (int): How many subdirectories to explore.                 A depth
    of 0 only explores the first subdirectory,                 while a depth of -1
    explores all subdirectories.     file_pattern (str): Valid regular expression
    denoting which                         files to yield in directory exploration.
    """
    file_re = re.compile(file_pattern)
    for x in os.listdir(directory):
        path = os.path.join(directory, x)
        if os.path.isdir(path):
            if file_re.search(path):
                yield path
            if depth != 0:
                for f in absolute_dirpaths(path, depth - 1, file_pattern):
                    yield f
