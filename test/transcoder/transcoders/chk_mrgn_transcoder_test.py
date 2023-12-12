from chkjson.model.chk.mrgn.decoded_mrgn_section import DecodedMrgnSection
from chkjson.transcoder.transcoders.chk_mrgn_transcoder import ChkMrgnTranscoder

from ...chk_resources import CHK_SECTION_FILE_PATHS


def _read_chk_section() -> bytes:
    with open(
        CHK_SECTION_FILE_PATHS[DecodedMrgnSection.section_name().value], "rb"
    ) as f:
        chk_binary_data = f.read()
    return chk_binary_data


def test_it_decodes_and_encodes_without_changing_data():
    transcoder: ChkMrgnTranscoder = ChkMrgnTranscoder()
    chk_binary_data = _read_chk_section()
    mrgn_section: DecodedMrgnSection = transcoder.decode(chk_binary_data)
    actual_encoded_data = transcoder.encode(mrgn_section, include_header=False)
    assert actual_encoded_data == chk_binary_data
    assert transcoder.decode(actual_encoded_data) == transcoder.decode(chk_binary_data)
