from chkjson.model.chk.upus.decoded_upus_section import DecodedUpusSection
from chkjson.transcoder.chk.transcoders.chk_upus_transcoder import ChkUpusTranscoder

from ....chk_resources import CHK_SECTION_FILE_PATHS


def _read_chk_section() -> bytes:
    with open(
        CHK_SECTION_FILE_PATHS[DecodedUpusSection.section_name().value], "rb"
    ) as f:
        chk_binary_data = f.read()
    return chk_binary_data


def test_it_decodes_expected_cuwp_slots_used():
    transcoder: ChkUpusTranscoder = ChkUpusTranscoder()
    chk_binary_data = _read_chk_section()
    section: DecodedUpusSection = transcoder.decode(chk_binary_data)
    # there's a single CUWP slot used in the map and its the first one
    assert section.cuwp_slots_used[0] == 1


def test_it_decodes_and_encodes_without_changing_data():
    transcoder: ChkUpusTranscoder = ChkUpusTranscoder()
    chk_binary_data = _read_chk_section()
    section: DecodedUpusSection = transcoder.decode(chk_binary_data)
    actual_encoded_data = transcoder.encode(section, include_header=False)
    assert actual_encoded_data == chk_binary_data
    assert transcoder.decode(actual_encoded_data) == transcoder.decode(chk_binary_data)
