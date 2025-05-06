from richchk.model.chk.ver.decoded_ver_section import DecodedVerSection
from richchk.transcoder.chk.transcoders.chk_ver_transcoder import ChkVerTranscoder

from ....chk_resources import CHK_SECTION_FILE_PATHS

# 205 - Brood War 1.00 (1.04)
_EXPECTED_VERSION = 205


def _read_chk_section() -> bytes:
    with open(
        CHK_SECTION_FILE_PATHS[DecodedVerSection.section_name().value], "rb"
    ) as f:
        chk_binary_data = f.read()
    return chk_binary_data


def test_it_decodes_expected_version():
    transcoder = ChkVerTranscoder()
    chk_binary_data = _read_chk_section()
    section = transcoder.decode(chk_binary_data)
    assert section.version == _EXPECTED_VERSION


def test_it_decodes_and_encodes_without_changing_data():
    transcoder = ChkVerTranscoder()
    chk_binary_data = _read_chk_section()
    section = transcoder.decode(chk_binary_data)
    actual_encoded_data = transcoder.encode(section, include_header=False)
    assert actual_encoded_data == chk_binary_data
    assert transcoder.decode(actual_encoded_data) == transcoder.decode(chk_binary_data)
