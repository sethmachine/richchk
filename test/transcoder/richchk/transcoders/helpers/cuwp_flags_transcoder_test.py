from richchk.model.richchk.uprp.flags.unit_property_flags import UnitPropertyFlags
from richchk.model.richchk.uprp.flags.valid_special_property_flags import (
    ValidSpecialPropertyFlags,
)
from richchk.model.richchk.uprp.flags.valid_unit_property_flags import (
    ValidUnitPropertyFlags,
)
from richchk.transcoder.richchk.transcoders.helpers.cuwp_flags_transcoder import (
    CuwpFlagsTranscoder,
)


def test_it_decodes_and_encodes_flags_for_unit_properties():
    # corresponds to all unit properties enabled
    # cloaked, burrowed, building in transit, hallucinated, invincible, unknown
    # 111111
    flags = 63
    expected_decoded_flags = UnitPropertyFlags(
        _cloaked=True,
        _burrowed=True,
        _building_in_transit=True,
        _hallucinated=True,
        _invincible=True,
        _unknown_flag=True,
    )
    _assert_flags_decode_and_encode_for_type(
        flags, expected_decoded_flags, UnitPropertyFlags
    )
    # 001001
    flags = 9
    expected_decoded_flags = UnitPropertyFlags(_cloaked=True, _hallucinated=True)
    _assert_flags_decode_and_encode_for_type(
        flags, expected_decoded_flags, UnitPropertyFlags
    )
    # 000000
    flags = 0
    expected_decoded_flags = UnitPropertyFlags()
    _assert_flags_decode_and_encode_for_type(
        flags, expected_decoded_flags, UnitPropertyFlags
    )


def test_it_decodes_and_encodes_flags_for_valid_unit_property_flags():
    # 1111111
    flags = 127
    expected_decoded_flags = ValidUnitPropertyFlags(
        _owner_play_valid=True,
        _hp_valid=True,
        _shields_valid=True,
        _energy_valid=True,
        _resource_amount_valid=True,
        _hanger_amount_valid=True,
        _unknown_flag=True,
    )
    _assert_flags_decode_and_encode_for_type(
        flags, expected_decoded_flags, ValidUnitPropertyFlags
    )
    # 0011001
    flags = 25
    expected_decoded_flags = ValidUnitPropertyFlags(
        _owner_play_valid=True,
        _hp_valid=False,
        _shields_valid=False,
        _energy_valid=True,
        _resource_amount_valid=True,
        _hanger_amount_valid=False,
        _unknown_flag=False,
    )
    _assert_flags_decode_and_encode_for_type(
        flags, expected_decoded_flags, ValidUnitPropertyFlags
    )
    # 0000000
    flags = 0
    expected_decoded_flags = ValidUnitPropertyFlags(
        _owner_play_valid=False,
        _hp_valid=False,
        _shields_valid=False,
        _energy_valid=False,
        _resource_amount_valid=False,
        _hanger_amount_valid=False,
        _unknown_flag=False,
    )
    _assert_flags_decode_and_encode_for_type(
        flags, expected_decoded_flags, ValidUnitPropertyFlags
    )


def test_it_decodes_and_encodes_flags_for_valid_special_property_flags():
    # 111111
    flags = 63
    expected_decoded_flags = ValidSpecialPropertyFlags(
        _cloak_valid=True,
        _burrowed_valid=True,
        _in_transit_valid=True,
        _hallucinated_valid=True,
        _invincible_valid=True,
        _unknown_flag=True,
    )
    _assert_flags_decode_and_encode_for_type(
        flags, expected_decoded_flags, ValidSpecialPropertyFlags
    )
    # 011001
    flags = 25
    expected_decoded_flags = ValidSpecialPropertyFlags(
        _cloak_valid=True,
        _burrowed_valid=False,
        _in_transit_valid=False,
        _hallucinated_valid=True,
        _invincible_valid=True,
        _unknown_flag=False,
    )
    _assert_flags_decode_and_encode_for_type(
        flags, expected_decoded_flags, ValidSpecialPropertyFlags
    )
    # 0000000
    flags = 0
    expected_decoded_flags = ValidSpecialPropertyFlags(
        _cloak_valid=False,
        _burrowed_valid=False,
        _in_transit_valid=False,
        _hallucinated_valid=False,
        _invincible_valid=False,
        _unknown_flag=False,
    )
    _assert_flags_decode_and_encode_for_type(
        flags, expected_decoded_flags, ValidSpecialPropertyFlags
    )


def _assert_flags_decode_and_encode_for_type(flags, expected_decoded_flags, flags_type):
    assert CuwpFlagsTranscoder.decode_flags(flags, flags_type) == expected_decoded_flags
    assert CuwpFlagsTranscoder.encode_flags(expected_decoded_flags) == flags
