"""As written these are all really integration tests since each test relies upon
ChkStrTranscoder to read the CHK binary data into a DecodedStrSection."""

import uuid

import pytest

from richchk.editor.chk.decoded_str_section_editor import DecodedStrSectionEditor
from richchk.io.richchk.rich_str_lookup_builder import RichStrLookupBuilder
from richchk.model.chk.str.decoded_str_section import DecodedStrSection
from richchk.transcoder.chk.transcoders.chk_str_transcoder import ChkStrTranscoder

from ...chk_resources import CHK_SECTION_FILE_PATHS

# these strings were added into the CHK section by using a GUI map editor
_EXPECTED_STRINGS = [
    "test-string-1-marine",
    "test-string-2-firebat",
    "test-string-3-ghost",
]


def _read_chk_section() -> bytes:
    with open(
        CHK_SECTION_FILE_PATHS[DecodedStrSection.section_name().value], "rb"
    ) as f:
        chk_binary_data = f.read()
    return chk_binary_data


@pytest.fixture(scope="function")
def str_section() -> DecodedStrSection:
    return ChkStrTranscoder().decode(_read_chk_section())


def test_it_does_not_modify_the_str_section_if_adding_already_existing_string(
    str_section,
):
    editor: DecodedStrSectionEditor = DecodedStrSectionEditor()
    new_str_section = editor.add_strings_to_str_section(
        [_EXPECTED_STRINGS[0]], str_section
    )
    assert new_str_section == str_section


def test_it_does_not_modify_the_str_section_if_adding_already_existing_strings(
    str_section,
):
    editor: DecodedStrSectionEditor = DecodedStrSectionEditor()
    new_str_section = editor.add_strings_to_str_section(_EXPECTED_STRINGS, str_section)
    assert new_str_section == str_section


def test_it_adds_a_new_string_and_modifies_str_as_expected(str_section):
    editor: DecodedStrSectionEditor = DecodedStrSectionEditor()
    string_to_add = str(uuid.uuid4())
    new_str_section = editor.add_strings_to_str_section([string_to_add], str_section)
    assert new_str_section != str_section
    assert string_to_add == new_str_section.strings[-1]
    assert new_str_section.number_of_strings == str_section.number_of_strings + 1
    assert len(new_str_section.strings_offsets) == len(str_section.strings_offsets) + 1
    assert len(new_str_section.strings) == len(str_section.strings) + 1
    assert new_str_section.strings[:-1] == str_section.strings


def test_adding_a_string_creates_a_valid_str_section(str_section):
    string_to_add = str(uuid.uuid4())
    new_str_section: DecodedStrSection = (
        DecodedStrSectionEditor().add_strings_to_str_section(
            [string_to_add], str_section
        )
    )
    decoded_new_str_section: DecodedStrSection = ChkStrTranscoder().decode(
        ChkStrTranscoder().encode(new_str_section, include_header=False)
    )
    assert decoded_new_str_section == new_str_section


def test_added_strings_have_correct_offsets(str_section):
    first_strings_to_add = [str(uuid.uuid4())]
    new_str = DecodedStrSectionEditor().add_strings_to_str_section(
        first_strings_to_add, str_section
    )
    _assert_string_offsets_are_valid(new_str)
    next_strings_to_add = [str(uuid.uuid4()), str(uuid.uuid4())]
    next_new_str = DecodedStrSectionEditor().add_strings_to_str_section(
        next_strings_to_add, str_section
    )
    _assert_string_offsets_are_valid(next_new_str)


def _assert_string_offsets_are_valid(str_section: DecodedStrSection):
    expected_strings = set(str_section.strings)
    found_strings = set()
    str_binary_data = ChkStrTranscoder().encode(str_section, include_header=False)
    for offset in str_section.strings_offsets:
        found_strings.add(
            RichStrLookupBuilder.get_rich_string_by_offset(
                offset=offset, str_binary_data=str_binary_data
            ).value
        )
    assert expected_strings == found_strings
