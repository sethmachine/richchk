"""As written these are all really integration tests since each test relies upon
ChkStrTranscoder to read the CHK binary data into a DecodedStrSection."""

import uuid

import pytest

from richchk.editor.chk.decoded_strx_section_editor import DecodedStrxSectionEditor
from richchk.model.chk.strx.decoded_strx_section import DecodedStrxSection
from richchk.transcoder.chk.transcoders.chk_strx_transcoder import ChkStrxTranscoder

from ...chk_resources import CHK_SECTION_FILE_PATHS
from .str_test_utils import assert_string_offsets_are_valid_for_strx

# these strings were added into the CHK section by using a GUI map editor
_EXPECTED_STRINGS = [
    "test-string-1-marine",
    "test-string-2-firebat",
    "test-string-3-ghost",
]


def _read_chk_section() -> bytes:
    with open(
        CHK_SECTION_FILE_PATHS[DecodedStrxSection.section_name().value], "rb"
    ) as f:
        chk_binary_data = f.read()
    return chk_binary_data


@pytest.fixture(scope="function")
def decoded_strx() -> DecodedStrxSection:
    return ChkStrxTranscoder().decode(_read_chk_section())


def test_it_does_not_modify_the_str_section_if_adding_only_already_existing_strings(
    decoded_strx,
):
    editor = DecodedStrxSectionEditor()
    new_str_section = editor.add_strings_to_strx_section(
        _EXPECTED_STRINGS, decoded_strx
    )
    assert new_str_section == decoded_strx
    assert_string_offsets_are_valid_for_strx(decoded_strx)


def test_it_adds_a_new_string_to_strx(decoded_strx):
    editor = DecodedStrxSectionEditor()
    string_to_add = str(uuid.uuid4())
    new_strx_section = editor.add_strings_to_strx_section([string_to_add], decoded_strx)
    _assert_it_encodes_and_decodes_new_strx_without_changes(new_strx_section)
    _assert_new_strings_are_added(new_strx_section, decoded_strx, [string_to_add])
    assert_string_offsets_are_valid_for_strx(decoded_strx)


def test_it_adds_multiple_strings_to_strx(decoded_strx):
    editor = DecodedStrxSectionEditor()
    strings_to_add = [str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4())]
    new_strx_section = editor.add_strings_to_strx_section(strings_to_add, decoded_strx)
    _assert_it_encodes_and_decodes_new_strx_without_changes(new_strx_section)
    _assert_new_strings_are_added(new_strx_section, decoded_strx, strings_to_add)
    assert_string_offsets_are_valid_for_strx(decoded_strx)


def test_it_only_adds_unique_strings_to_strx(decoded_strx):
    editor = DecodedStrxSectionEditor()
    same_string = str(uuid.uuid4())
    different_string = str(uuid.uuid4())
    strings_to_add = [same_string, same_string, different_string]
    expected_strings_to_add = [same_string, different_string]
    new_strx_section = editor.add_strings_to_strx_section(strings_to_add, decoded_strx)
    _assert_it_encodes_and_decodes_new_strx_without_changes(new_strx_section)
    _assert_new_strings_are_added(
        new_strx_section, decoded_strx, expected_strings_to_add
    )


def test_it_adds_more_than_u16_strings(decoded_strx):
    max_u16 = 65535 + 10
    strings_to_add = [str(uuid.uuid4()) for x in range(0, max_u16)]
    editor = DecodedStrxSectionEditor()
    new_strx = editor.add_strings_to_strx_section(strings_to_add, decoded_strx)
    _assert_new_strings_are_added(new_strx, decoded_strx, strings_to_add)
    assert_string_offsets_are_valid_for_strx(decoded_strx)


def _assert_it_encodes_and_decodes_new_strx_without_changes(strx_section):
    """Verifies no unexpected changes to the binary format when modify the section."""
    transcoder = ChkStrxTranscoder()
    assert strx_section == transcoder.decode(
        transcoder.encode(strx_section, include_header=False)
    )


def _assert_new_strings_are_added(new_strx, old_strx, strings_added):
    index_for_newly_added_strings = len(strings_added) * -1
    assert strings_added == new_strx.strings[index_for_newly_added_strings:]
    assert new_strx.number_of_strings == old_strx.number_of_strings + len(strings_added)
    assert len(new_strx.strings_offsets) == (
        len(old_strx.strings_offsets) + len(strings_added)
    )
    assert len(new_strx.strings) == (len(old_strx.strings) + len(strings_added))
    assert new_strx.strings[:index_for_newly_added_strings] == old_strx.strings
