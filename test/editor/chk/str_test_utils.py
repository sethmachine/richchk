from richchk.io.richchk.rich_str_lookup_builder import RichStrLookupBuilder
from richchk.model.chk.str.decoded_str_section import DecodedStrSection
from richchk.model.chk.strx.decoded_strx_section import DecodedStrxSection
from richchk.transcoder.chk.transcoders.chk_str_transcoder import ChkStrTranscoder
from richchk.transcoder.chk.transcoders.chk_strx_transcoder import ChkStrxTranscoder


def assert_string_offsets_are_valid_for_str(str_section: DecodedStrSection):
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


def assert_string_offsets_are_valid_for_strx(str_section: DecodedStrxSection):
    expected_strings = set(str_section.strings)
    found_strings = set()
    str_binary_data = ChkStrxTranscoder().encode(str_section, include_header=False)
    for offset in str_section.strings_offsets:
        found_strings.add(
            RichStrLookupBuilder.get_rich_string_by_offset(
                offset=offset, str_binary_data=str_binary_data
            ).value
        )
    assert expected_strings == found_strings
