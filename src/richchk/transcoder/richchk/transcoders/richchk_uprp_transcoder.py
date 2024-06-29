"""Decode UPRP.

Required for all versions. Not required for Melee. Validation: Must be size of 1280
bytes.

This section is used whenever the create units with properties trigger is used. Since a
slot has to be assigned to the action, this is where each slot is designated.

There are 64 of the following structures regardless of how many are used and it cannot
exceed 64.

u16: Flag of which special properties can be applied to unit, and are valid.

Bit 0 - Cloak bit is valid

Bit 1 - Burrowed bit is valid

Bit 2 - In transit bit is valid

Bit 3 - Hallucinated bit is valid

Bit 4 - Invincible bit is valid

Bit 5-15 - Unknown/unused

u16: Which elements of the unit data are valid, which properties can be changed by the
map maker.

Bit 0 - Owner player is valid (unit is not neutral)

Bit 1 - HP is valid

Bit 2 - Shields is valid

Bit 3 - Energy is valid

Bit 4 - Resource amount is valid (unit is a resource)

Bit 5 - Amount in hanger is valid

Bit 6 - Unknown/unused

u8: Player number that owns unit. Will always be NULL in this section (0)

u8: Hit point % (1-100)

u8: Shield point % (1-100)

u8: Energy point % (1-100)

u32: Resource amount (for resources only)

u16: # of units in hangar

u16: Flags

Bit 0 - Unit is cloaked

Bit 1 - Unit is burrowed

Bit 2 - Building is in transit

Bit 3 - Unit is hallucinated

Bit 4 - Unit is invincible

Bit 5-15 - Unknown/unused

u32: Unknown/unused. Padding?
"""

from ....model.chk.uprp.decoded_cuwp_slot import DecodedCuwpSlot
from ....model.chk.uprp.decoded_uprp_section import DecodedUprpSection
from ....model.chk.uprp.uprp_constants import MAX_CUWP_SLOTS
from ....model.richchk.richchk_decode_context import RichChkDecodeContext
from ....model.richchk.richchk_encode_context import RichChkEncodeContext
from ....model.richchk.uprp.flags.unit_property_flags import UnitPropertyFlags
from ....model.richchk.uprp.flags.valid_special_property_flags import (
    ValidSpecialPropertyFlags,
)
from ....model.richchk.uprp.flags.valid_unit_property_flags import (
    ValidUnitPropertyFlags,
)
from ....model.richchk.uprp.rich_cuwp_slot import RichCuwpSlot, _RichCuwpSlotFlagsData
from ....model.richchk.uprp.rich_uprp_section import RichUprpSection
from ....transcoder.richchk.richchk_section_transcoder import RichChkSectionTranscoder
from ....transcoder.richchk.richchk_section_transcoder_factory import (
    _RichChkRegistrableTranscoder,
)
from ....util import logger
from .helpers.cuwp_flags_transcoder import CuwpFlagsTranscoder


class RichChkUprpTranscoder(
    RichChkSectionTranscoder[RichUprpSection, DecodedUprpSection],
    _RichChkRegistrableTranscoder,
    chk_section_name=DecodedUprpSection.section_name(),
):
    def __init__(self) -> None:
        self.log = logger.get_logger(RichChkUprpTranscoder.__name__)

    def decode(
        self,
        decoded_chk_section: DecodedUprpSection,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> RichUprpSection:
        cuwp_slots: list[RichCuwpSlot] = []
        for index, cuwp in enumerate(decoded_chk_section.cuwp_slots):
            if not self._is_unused_cuwp_slot(cuwp):
                cuwp_slots.append(self._decode_cuwp_slot(cuwp, index))
        return RichUprpSection(_cuwp_slots=cuwp_slots)

    def _decode_cuwp_slot(
        self, decoded_cuwp_slot: DecodedCuwpSlot, index: int
    ) -> RichCuwpSlot:
        valid_special_property_flags = CuwpFlagsTranscoder.decode_flags(
            decoded_cuwp_slot.valid_special_properties_flags, ValidSpecialPropertyFlags
        )
        valid_unit_property_flags = CuwpFlagsTranscoder.decode_flags(
            decoded_cuwp_slot.valid_unit_properties_flags, ValidUnitPropertyFlags
        )
        unit_property_flags = CuwpFlagsTranscoder.decode_flags(
            decoded_cuwp_slot.flags, UnitPropertyFlags
        )

        return RichCuwpSlot(
            _hitpoints_percentage=decoded_cuwp_slot.hitpoints_percentage,
            _shieldpoints_percentage=decoded_cuwp_slot.shieldpoints_percentage,
            _energypoints_percentage=decoded_cuwp_slot.energypoints_percentage,
            _resource_amount=decoded_cuwp_slot.resource_amount,
            _units_in_hangar=decoded_cuwp_slot.units_in_hangar,
            _cloaked=unit_property_flags.cloaked,
            _burrowed=unit_property_flags.burrowed,
            _building_in_transit=unit_property_flags.building_in_transit,
            _hallucinated=unit_property_flags.hallucinated,
            _invincible=unit_property_flags.invincible,
            _flags_data=_RichCuwpSlotFlagsData(
                _valid_special_property_flags=valid_special_property_flags,
                _valid_unit_property_flags=valid_unit_property_flags,
                _unknown_flag=unit_property_flags.unknown_flag,
                _padding=decoded_cuwp_slot.padding,
            ),
            # CUWP are referenced 1-based not 0-based index
            _index=index + 1,
        )

    @classmethod
    def _is_unused_cuwp_slot(cls, decoded_cuwp_slot: DecodedCuwpSlot) -> bool:
        """Filter out empty/placeholder locations from the DecodedUprpSection.

        :param decoded_cuwp_slot:
        :return:
        """
        return (
            decoded_cuwp_slot.valid_special_properties_flags == 0
            and decoded_cuwp_slot.valid_unit_properties_flags == 0
            and decoded_cuwp_slot.owner_player == 0
            and decoded_cuwp_slot.hitpoints_percentage == 0
            and decoded_cuwp_slot.shieldpoints_percentage == 0
            and decoded_cuwp_slot.energypoints_percentage == 0
            and decoded_cuwp_slot.resource_amount == 0
            and decoded_cuwp_slot.units_in_hangar == 0
            and decoded_cuwp_slot.flags == 0
            and decoded_cuwp_slot.padding == 0
        )

    def encode(
        self,
        rich_chk_section: RichUprpSection,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedUprpSection:
        decoded_cuwp_slots: list[DecodedCuwpSlot] = []
        assert all((cuwp.index is not None for cuwp in rich_chk_section.cuwp_slots))
        cuwp_by_index = {
            cuwp.index - 1: cuwp
            for cuwp in rich_chk_section.cuwp_slots
            if cuwp.index is not None
        }
        for index in range(0, MAX_CUWP_SLOTS):
            maybe_cuwp = cuwp_by_index.get(index, None)
            if not maybe_cuwp:
                decoded_cuwp_slots.append(self._generate_unused_cuwp_slot())
            else:
                decoded_cuwp_slots.append(self._encode_cuwp_slot(maybe_cuwp))
        return DecodedUprpSection(_cuwp_slots=decoded_cuwp_slots)

    def _encode_cuwp_slot(self, cuwp_slot: RichCuwpSlot) -> DecodedCuwpSlot:
        return DecodedCuwpSlot(
            _valid_special_properties_flags=CuwpFlagsTranscoder.encode_flags(
                cuwp_slot.flags_data.valid_special_property_flags
            ),
            _valid_unit_properties_flags=CuwpFlagsTranscoder.encode_flags(
                cuwp_slot.flags_data.valid_unit_property_flags
            ),
            # owner player should always be 0/null
            _owner_player=0,
            _hitpoints_percentage=cuwp_slot.hitpoints_percentage,
            _shieldpoints_percentage=cuwp_slot.shieldpoints_percentage,
            _energypoints_percentage=cuwp_slot.energypoints_percentage,
            _resource_amount=cuwp_slot.resource_amount,
            _units_in_hangar=cuwp_slot.units_in_hangar,
            _flags=CuwpFlagsTranscoder.encode_flags(
                UnitPropertyFlags(
                    _cloaked=cuwp_slot.cloaked,
                    _burrowed=cuwp_slot.burrowed,
                    _building_in_transit=cuwp_slot.building_in_transit,
                    _hallucinated=cuwp_slot.hallucinated,
                    _invincible=cuwp_slot.invincible,
                    _unknown_flag=cuwp_slot.flags_data.unknown_flag,
                )
            ),
            _padding=cuwp_slot.flags_data.padding,
        )

    @classmethod
    def _generate_unused_cuwp_slot(cls) -> DecodedCuwpSlot:
        """Generate filler CUWP data to fill in any CUWP slots."""
        return DecodedCuwpSlot(
            _valid_special_properties_flags=0,
            _valid_unit_properties_flags=0,
            _owner_player=0,
            _hitpoints_percentage=0,
            _shieldpoints_percentage=0,
            _energypoints_percentage=0,
            _resource_amount=0,
            _units_in_hangar=0,
            _flags=0,
            _padding=0,
        )
