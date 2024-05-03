"""End-to-end test that edits a RichChk and asserts the changes are made as expected."""

import uuid
from typing import TypeVar

import pytest

from chkjson.editor.richchk.rich_chk_editor import RichChkEditor
from chkjson.editor.richchk.rich_mrgn_editor import RichMrgnEditor
from chkjson.io.chk.chk_io import ChkIo
from chkjson.io.richchk.richchk_io import RichChkIo
from chkjson.io.util.chk_query_util import ChkQueryUtil
from chkjson.model.chk.decoded_chk_section import DecodedChkSection
from chkjson.model.chk_section_name import ChkSectionName
from chkjson.model.richchk.mrgn.rich_location import RichLocation
from chkjson.model.richchk.mrgn.rich_mrgn_section import RichMrgnSection
from chkjson.model.richchk.rich_chk import RichChk
from chkjson.model.richchk.str.rich_string import RichString

from ..chk_resources import SCX_CHK_FILE
from ..helpers.dataclasses_helper import compare_dataclasses_ignoring_fields

T = TypeVar("T", bound=DecodedChkSection, covariant=True)


@pytest.fixture(scope="function")
def chk_output_file_path(tmpdir_factory):
    return tmpdir_factory.mktemp("chk_io_test-output-files").join(
        f"{str(uuid.uuid4())}.chk"
    )


@pytest.fixture(scope="function")
def rich_chk_for_scx_file() -> RichChk:
    decoded_chk = ChkIo().decode_chk_file(SCX_CHK_FILE)
    rich_chk = RichChkIo().decode_chk(decoded_chk)
    return rich_chk


def test_integration_it_edits_mrgn_in_rich_chk(
    rich_chk_for_scx_file, chk_output_file_path
):
    mrgn = ChkQueryUtil.find_only_rich_section_in_chk(
        ChkSectionName.MRGN, rich_chk_for_scx_file
    )
    assert isinstance(mrgn, RichMrgnSection)
    new_location = RichLocation(
        _left_x1=10,
        _top_y1=20,
        _right_x2=30,
        _bottom_y2=40,
        _custom_location_name=RichString(_value="new location"),
    )
    expected_locations = mrgn.locations + [new_location]
    new_mrgn = RichMrgnEditor().add_locations([new_location], mrgn)
    _assert_all_locations_have_index(new_mrgn.locations)
    _assert_mrgn_has_expected_locations_ignoring_index(expected_locations, new_mrgn)
    new_rich_chk = RichChkEditor().replace_chk_section(new_mrgn, rich_chk_for_scx_file)
    _assert_rich_chk_has_expected_mrgn_section(new_mrgn, new_rich_chk)
    # now encode all the way back to a chk file, and then back to RichChk
    # the expected locations should still exist
    ChkIo().encode_chk_to_file(
        RichChkIo().encode_chk(new_rich_chk), chk_output_file_path
    )
    rich_chk_again = RichChkIo().decode_chk(
        ChkIo().decode_chk_file(chk_output_file_path)
    )
    _assert_rich_chk_has_expected_mrgn_section(new_mrgn, rich_chk_again)
    rich_mrgn_again = ChkQueryUtil.find_only_rich_section_in_chk(
        ChkSectionName.MRGN, rich_chk_again
    )
    assert isinstance(rich_mrgn_again, RichMrgnSection)
    _assert_mrgn_has_expected_locations_ignoring_index(
        expected_locations, rich_mrgn_again
    )


def _assert_all_locations_have_index(locations: list[RichLocation]):
    for loc in locations:
        assert loc.index is not None


def _assert_rich_chk_has_expected_mrgn_section(
    expected_mrgn: RichMrgnSection, rich_chk
):
    actual_mrgn = ChkQueryUtil.find_only_rich_section_in_chk(
        ChkSectionName.MRGN, rich_chk
    )
    assert isinstance(actual_mrgn, RichMrgnSection)
    assert set(actual_mrgn.locations) == set(expected_mrgn.locations)


def _assert_mrgn_has_expected_locations_ignoring_index(
    expected_locations: list[RichLocation], mrgn: RichMrgnSection
):
    for expected in expected_locations:
        assert any(
            (
                compare_dataclasses_ignoring_fields(expected, actual)
                for actual in mrgn.locations
            )
        )
