"""Points to an open file handle used for searching files in an MPQ archive."""

from ctypes import c_void_p


class StormLibMpqHandle(c_void_p):
    def __repr__(self) -> str:
        maybe_id = id(self)
        assert maybe_id is not None
        assert self.value is not None
        return "<StormLibMpqHandle object at %s: %s>" % (
            hex(maybe_id),
            hex(self.value),
        )
