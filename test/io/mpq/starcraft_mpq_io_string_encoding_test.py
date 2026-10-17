import shutil

import pytest

from richchk.io.mpq.starcraft_mpq_io import StarCraftMpqIo
from richchk.io.richchk.query.chk_query_util import ChkQueryUtil
from richchk.util.fileutils import CrossPlatformSafeTemporaryNamedFile

from ...chk_resources import EXAMPLE_STARCRAFT_SCX_MAP


def _string_section(chk):
    return ChkQueryUtil.find_string_section_in_chk(chk)


def _read(embedded_stormlib, **kwargs):
    with CrossPlatformSafeTemporaryNamedFile() as temp_scx_file:
        shutil.copy(EXAMPLE_STARCRAFT_SCX_MAP, temp_scx_file)
        return _string_section(
            StarCraftMpqIo(
                embedded_stormlib, **kwargs.pop("init", {})
            ).read_chk_from_mpq(temp_scx_file, **kwargs)
        )


@pytest.mark.usefixtures("embedded_stormlib")
def test_read_detects_utf8_by_default(embedded_stormlib):
    if embedded_stormlib:
        assert _read(embedded_stormlib).encoding == "utf-8"


@pytest.mark.usefixtures("embedded_stormlib")
def test_read_with_explicit_encoding_keeps_the_text(embedded_stormlib):
    if embedded_stormlib:
        auto = _read(embedded_stormlib)
        explicit = _read(embedded_stormlib, string_encoding="cp949")
        assert explicit.encoding == "cp949"
        # the example map's strings are ASCII, so they read the same in any encoding
        assert explicit.strings == auto.strings
        assert explicit.strings_offsets == auto.strings_offsets


@pytest.mark.usefixtures("embedded_stormlib")
def test_read_uses_the_encoding_given_to_the_class(embedded_stormlib):
    if embedded_stormlib:
        assert (
            _read(embedded_stormlib, init={"string_encoding": "cp949"}).encoding
            == "cp949"
        )
        # an encoding given to the read overrides the class's
        assert (
            _read(
                embedded_stormlib,
                init={"string_encoding": "cp949"},
                string_encoding="gbk",
            ).encoding
            == "gbk"
        )
        # "auto" on the read goes back to detecting
        assert (
            _read(
                embedded_stormlib,
                init={"string_encoding": "cp949"},
                string_encoding="auto",
            ).encoding
            == "utf-8"
        )


@pytest.mark.usefixtures("embedded_stormlib")
def test_invalid_encoding_is_rejected(embedded_stormlib):
    if embedded_stormlib:
        with pytest.raises(ValueError):
            StarCraftMpqIo(embedded_stormlib, string_encoding="not-a-codec")
        with pytest.raises(ValueError):
            StarCraftMpqIo(embedded_stormlib).read_chk_from_mpq(
                EXAMPLE_STARCRAFT_SCX_MAP, string_encoding="utf-16"
            )
