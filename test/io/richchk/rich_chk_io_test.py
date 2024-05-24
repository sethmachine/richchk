import unittest
import uuid
from test.chk_resources import DEMON_LORE_YATAPI_TEST_CHK_FILE_PATH, SCX_CHK_FILE
from typing import TypeVar

import pytest

from chkjson.io.chk.chk_io import ChkIo
from chkjson.io.richchk.richchk_io import RichChkIo
from chkjson.model.chk.decoded_chk import DecodedChk
from chkjson.model.chk.decoded_chk_section import DecodedChkSection
from chkjson.model.chk.mrgn.decoded_mrgn_section import DecodedMrgnSection
from chkjson.model.chk.str.decoded_str_section import DecodedStrSection
from chkjson.model.chk.trig.decoded_trig_section import DecodedTrigSection
from chkjson.model.chk.unis.decoded_unis_section import DecodedUnisSection
from chkjson.model.chk.unknown.decoded_unknown_section import DecodedUnknownSection
from chkjson.model.chk_section_name import ChkSectionName
from chkjson.model.richchk.rich_chk import RichChk
from chkjson.model.richchk.rich_chk_section import RichChkSection
from chkjson.model.richchk.unis.rich_unis_section import RichUnisSection
from chkjson.transcoder.richchk.richchk_section_transcoder_factory import (
    RichChkSectionTranscoderFactory,
)

T = TypeVar("T", bound=DecodedChkSection, covariant=True)


@pytest.fixture(scope="function")
def chk_output_file_path(tmpdir_factory):
    return tmpdir_factory.mktemp("chk_io_test-output-files").join(
        f"{str(uuid.uuid4())}.chk"
    )


def test_integration_rich_chk_io_decodes_decoded_chk():
    richhk_io = RichChkIo()
    chk: DecodedChk = DecodedChk(
        _decoded_chk_sections=[
            DecodedUnknownSection(ChkSectionName.UNKNOWN.value, b""),
            DecodedStrSection(_number_of_strings=0, _string_offsets=[], _strings=[]),
            DecodedMrgnSection(_locations=[]),
            DecodedUnisSection([], [], [], [], [], [], [], [], [], []),
        ]
    )
    rich_chk: RichChk = richhk_io.decode_chk(chk)
    assert len(rich_chk.chk_sections) == len(chk.decoded_chk_sections)
    assert len(rich_chk.get_sections_by_name(ChkSectionName.UNKNOWN)) == 1
    assert isinstance(
        rich_chk.get_sections_by_name(ChkSectionName.UNKNOWN)[0], DecodedUnknownSection
    )
    assert len(rich_chk.get_sections_by_name(ChkSectionName.STR)) == 1
    assert isinstance(
        rich_chk.get_sections_by_name(ChkSectionName.STR)[0], DecodedStrSection
    )
    assert len(rich_chk.get_sections_by_name(ChkSectionName.UNIS)) == 1
    assert isinstance(
        rich_chk.get_sections_by_name(ChkSectionName.UNIS)[0], RichUnisSection
    )


def test_integration_rich_chk_io_decodes_decoded_chk_into_all_sections():
    chkio = ChkIo()
    richhk_io = RichChkIo()
    chk: DecodedChk = chkio.decode_chk_file(DEMON_LORE_YATAPI_TEST_CHK_FILE_PATH)
    rich_chk: RichChk = richhk_io.decode_chk(chk)
    assert len(chk.decoded_chk_sections) == len(rich_chk.chk_sections)
    assert_all_supported_rich_chk_sections_are_present(rich_chk)


def test_integration_rich_chk_io_decodes_and_encodes_back_unchanged():
    # this test could break, probably better to verify
    # you can get the same rich chk again
    chkio = ChkIo()
    richhk_io = RichChkIo()
    chk: DecodedChk = chkio.decode_chk_file(DEMON_LORE_YATAPI_TEST_CHK_FILE_PATH)
    rich_chk: RichChk = richhk_io.decode_chk(chk)
    actual_encoded_chk: DecodedChk = richhk_io.encode_chk(rich_chk)
    assert_chks_are_equal(actual_encoded_chk, chk)


def test_integration_rich_chk_io_decodes_decoded_chk_into_all_sections_for_scx_file():
    chkio = ChkIo()
    richhk_io = RichChkIo()
    chk: DecodedChk = chkio.decode_chk_file(SCX_CHK_FILE)
    rich_chk: RichChk = richhk_io.decode_chk(chk)
    assert len(chk.decoded_chk_sections) == len(rich_chk.chk_sections)
    assert_all_supported_rich_chk_sections_are_present(rich_chk)


def test_integration_rich_chk_io_decodes_and_encodes_back_unchanged_for_scx_file():
    # this test could break, probably better to verify
    # you can get the same rich chk again
    chkio = ChkIo()
    richhk_io = RichChkIo()
    chk: DecodedChk = chkio.decode_chk_file(SCX_CHK_FILE)
    rich_chk: RichChk = richhk_io.decode_chk(chk)
    actual_encoded_chk: DecodedChk = richhk_io.encode_chk(rich_chk)
    assert_chks_are_equal(actual_encoded_chk, chk)


def assert_all_supported_rich_chk_sections_are_present(rich_chk: RichChk):
    """All supported RichChkSections are present in the RichChk."""
    for (
        chk_section_name
    ) in RichChkSectionTranscoderFactory.get_all_registered_chk_section_names():
        assert len(rich_chk.get_sections_by_name(chk_section_name)) == 1
        assert isinstance(
            rich_chk.get_sections_by_name(chk_section_name)[0], RichChkSection
        )


def assert_chks_are_equal(decoded_chk1: DecodedChk, decoded_chk2: DecodedChk):
    assert len(decoded_chk1.decoded_chk_sections) == len(
        decoded_chk2.decoded_chk_sections
    )
    for index, section in enumerate(decoded_chk1.decoded_chk_sections):
        if isinstance(section, DecodedTrigSection):
            unittest.TestCase().assertEqual(
                section,
                decoded_chk2.decoded_chk_sections[index],
                "Actual trig section does not match expected trig section!",
            )
        else:
            assert section == decoded_chk2.decoded_chk_sections[index]
