"""File system utility functions to simplify file manipulation."""

import os
import re
from typing import Iterator


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
