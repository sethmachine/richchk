import shutil

import pytest

from richchk.io.mpq.starcraft_mpq_io import StarCraftMpqIo
from richchk.io.richchk.query.chk_query_util import ChkQueryUtil

from ...chk_resources import EXAMPLE_STARCRAFT_SCX_MAP

_NON_ASCII_NAMES = ["중세유럽제국_F5.62.scx", "魔兽争霸_测试.scx", "café ünïcode.scx"]


@pytest.mark.usefixtures("embedded_stormlib")
@pytest.mark.parametrize("file_name", _NON_ASCII_NAMES)
def test_it_reads_a_map_whose_file_name_is_not_ascii(
    embedded_stormlib, tmp_path, file_name
):
    if embedded_stormlib:
        map_path = tmp_path / file_name
        shutil.copy(EXAMPLE_STARCRAFT_SCX_MAP, map_path)
        chk = StarCraftMpqIo(embedded_stormlib).read_chk_from_mpq(str(map_path))
        assert ChkQueryUtil.find_string_section_in_chk(chk).strings


@pytest.mark.usefixtures("embedded_stormlib")
@pytest.mark.parametrize("file_name", _NON_ASCII_NAMES)
def test_it_saves_a_map_to_a_file_name_that_is_not_ascii(
    embedded_stormlib, tmp_path, file_name
):
    if embedded_stormlib:
        mpq_io = StarCraftMpqIo(embedded_stormlib)
        chk = mpq_io.read_chk_from_mpq(EXAMPLE_STARCRAFT_SCX_MAP)
        output_path = tmp_path / file_name
        mpq_io.save_chk_to_mpq(
            chk, EXAMPLE_STARCRAFT_SCX_MAP, str(output_path), overwrite_existing=False
        )
        assert output_path.exists()
        reread = mpq_io.read_chk_from_mpq(str(output_path))
        assert (
            ChkQueryUtil.find_string_section_in_chk(reread).strings
            == ChkQueryUtil.find_string_section_in_chk(chk).strings
        )


@pytest.mark.usefixtures("embedded_stormlib")
def test_it_extracts_the_chk_to_a_file_name_that_is_not_ascii(
    embedded_stormlib, tmp_path
):
    if embedded_stormlib:
        output_path = tmp_path / "중세유럽제국.chk"
        StarCraftMpqIo(embedded_stormlib).extract_chk_from_mpq(
            EXAMPLE_STARCRAFT_SCX_MAP, str(output_path)
        )
        assert output_path.stat().st_size > 0
