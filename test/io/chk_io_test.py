import os
import uuid
from typing import TypeVar

import pytest

from chkjson.io.chk_io import ChkIo
from chkjson.model.chk.decoded_chk import DecodedChk
from chkjson.model.chk.decoded_chk_section import DecodedChkSection
from chkjson.model.chk.unknown.decoded_unknown_section import DecodedUnknownSection
from chkjson.model.chk_section_name import ChkSectionName
from chkjson.transcoder.chk_section_transcoder_factory import (
    ChkSectionTranscoderFactory,
)

from ..chk_resources import DEMON_LORE_YATAPI_TEST_CHK_FILE_PATH

T = TypeVar("T", bound=DecodedChkSection, covariant=True)


@pytest.fixture(scope="function")
def chk_output_file_path(tmpdir_factory):
    return tmpdir_factory.mktemp("chk_io_test-output-files").join(
        f"{str(uuid.uuid4())}.chk"
    )


def test_chk_io_decodes_chk_file_into_all_sections():
    chkio = ChkIo()
    chk: DecodedChk = chkio.decode_chk_file(DEMON_LORE_YATAPI_TEST_CHK_FILE_PATH)
    _assert_decoded_chk_has_expected_decoded_sections(chk)


def test_chk_io_decodes_chk_binary_data_into_all_sections():
    chkio = ChkIo()
    with open(DEMON_LORE_YATAPI_TEST_CHK_FILE_PATH, "rb") as f:
        chk_binary_data = f.read()
    chk: DecodedChk = chkio.decode_chk_binary_data(chk_binary_data)
    _assert_decoded_chk_has_expected_decoded_sections(chk)


def test_chk_io_it_decodes_and_encodes_without_changing_data():
    chkio = ChkIo()
    with open(DEMON_LORE_YATAPI_TEST_CHK_FILE_PATH, "rb") as f:
        chk_binary_data = f.read()
    chk: DecodedChk = chkio.decode_chk_binary_data(chk_binary_data)
    _assert_decoded_chk_has_expected_decoded_sections(chk)
    encoded_chk: bytes = chkio.encode_chk_to_bytes(chk)
    assert encoded_chk == chk_binary_data


def test_chk_io_it_encodes_to_output_file_without_changing_data(chk_output_file_path):
    chkio = ChkIo()
    chk: DecodedChk = chkio.decode_chk_file(DEMON_LORE_YATAPI_TEST_CHK_FILE_PATH)
    _assert_decoded_chk_has_expected_decoded_sections(chk)
    chkio.encode_chk_to_file(chk, chk_output_file_path)
    assert os.path.exists(chk_output_file_path)
    output_chk: DecodedChk = chkio.decode_chk_file(chk_output_file_path)
    _assert_decoded_chk_has_expected_decoded_sections(output_chk)
    expected_chk_data: bytes = chkio.encode_chk_to_bytes(chk)
    output_chk_data: bytes = chkio.encode_chk_to_bytes(output_chk)
    assert output_chk_data == expected_chk_data


def _assert_decoded_chk_has_expected_decoded_sections(chk: DecodedChk):
    section_by_name = {
        _get_actual_section_name_for_chk_section(section): section
        for section in chk.decoded_chk_sections
    }
    expected_decoded_section_names: set[ChkSectionName] = {
        x for x in ChkSectionName
    }.intersection(
        {x for x in ChkSectionTranscoderFactory.get_all_registered_chk_section_names()}
    )
    for expected_section_name in expected_decoded_section_names:
        assert expected_section_name.value in section_by_name


def _get_actual_section_name_for_chk_section(
    decoded_chk_section: DecodedChkSection,
) -> str:
    """Resolve a DecodedChkSection to its actual CHK section name.

    This handles the edge case where the UnknownChkSection stores the actual name in a
    field variable.

    :param decoded_chk_section:
    :return:
    """
    if isinstance(decoded_chk_section, DecodedUnknownSection):
        unknown_section: DecodedUnknownSection = DecodedChkSection.cast(
            decoded_chk_section, DecodedUnknownSection
        )
        return unknown_section.actual_section_name
    return decoded_chk_section.section_name().value
