from chkjson.model.chk.uprp.decoded_cuwp_slot import DecodedCuwpSlot
from chkjson.model.chk.uprp.decoded_uprp_section import DecodedUprpSection
from chkjson.transcoder.chk.transcoders.chk_uprp_transcoder import ChkUprpTranscoder

from ....chk_resources import CHK_SECTION_FILE_PATHS


def _read_chk_section() -> bytes:
    with open(
        CHK_SECTION_FILE_PATHS[DecodedUprpSection.section_name().value], "rb"
    ) as f:
        chk_binary_data = f.read()
    return chk_binary_data


# 37 Tom Kazansky Wraiths with 33% hp, 35% shields, 34% energy, hallucinated + cloaked
_EXPECTED_DECODED_CUWP_SLOT = DecodedCuwpSlot(
    _valid_special_properties_flags=31,
    _valid_unit_properties_flags=63,
    _owner_player=0,
    _hitpoints_percentage=33,
    _shieldpoints_percentage=35,
    _energypoints_percentage=34,
    _resource_amount=0,
    _units_in_hangar=0,
    _flags=9,
    _padding=0,
)


def test_it_decodes_expected_cuwp_slot():
    transcoder: ChkUprpTranscoder = ChkUprpTranscoder()
    chk_binary_data = _read_chk_section()
    uprp_section: DecodedUprpSection = transcoder.decode(chk_binary_data)
    assert _EXPECTED_DECODED_CUWP_SLOT in uprp_section.cuwp_slots


def test_it_decodes_and_encodes_without_changing_data():
    transcoder: ChkUprpTranscoder = ChkUprpTranscoder()
    chk_binary_data = _read_chk_section()
    uprp_section: DecodedUprpSection = transcoder.decode(chk_binary_data)
    actual_encoded_data = transcoder.encode(uprp_section, include_header=False)
    assert actual_encoded_data == chk_binary_data
    assert transcoder.decode(actual_encoded_data) == transcoder.decode(chk_binary_data)
