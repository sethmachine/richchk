from richchk.model.chk.swnm.decoded_swnm_section import DecodedSwnmSection
from richchk.transcoder.chk.transcoders.chk_swnm_transcoder import ChkSwnmTranscoder

from ....chk_resources import CHK_SECTION_FILE_PATHS


def _read_chk_section() -> bytes:
    with open(
        CHK_SECTION_FILE_PATHS[DecodedSwnmSection.section_name().value], "rb"
    ) as f:
        chk_binary_data = f.read()
    return chk_binary_data


def test_it_decodes_expected_switch_string_ids():
    transcoder: ChkSwnmTranscoder = ChkSwnmTranscoder()
    chk_binary_data = _read_chk_section()
    swnm = transcoder.decode(chk_binary_data)
    assert len(swnm.switch_string_ids) == ChkSwnmTranscoder.NUM_SWITCHES
    # switches 4, 5, 7 were given strings so their string IDs should be non-zero
    # switches are zero indexed in thw SWNM
    assert swnm.switch_string_ids[:3] == [0, 0, 0]
    assert swnm.switch_string_ids[3] != 0
    assert swnm.switch_string_ids[4] != 0
    assert swnm.switch_string_ids[6] != 0
    assert all(x == 0 for x in swnm.switch_string_ids[7:])


def test_it_decodes_and_encodes_without_changing_data():
    transcoder: ChkSwnmTranscoder = ChkSwnmTranscoder()
    chk_binary_data = _read_chk_section()
    swnm = transcoder.decode(chk_binary_data)
    actual_encoded_data = transcoder.encode(swnm, include_header=False)
    assert actual_encoded_data == chk_binary_data
    assert transcoder.decode(actual_encoded_data) == transcoder.decode(chk_binary_data)
