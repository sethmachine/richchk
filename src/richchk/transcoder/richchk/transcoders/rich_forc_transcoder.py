"""Decode and encode the FORC - Force Settings section."""

from ....model.chk.forc.decoded_forc_section import DecodedForcSection
from ....model.richchk.forc.force_flags import ForceFlags
from ....model.richchk.forc.force_id import ForceId
from ....model.richchk.forc.rich_forc_section import RichForcSection
from ....model.richchk.forc.rich_force import RichForce
from ....model.richchk.richchk_decode_context import RichChkDecodeContext
from ....model.richchk.richchk_encode_context import RichChkEncodeContext
from ....transcoder.richchk.richchk_section_transcoder import RichChkSectionTranscoder
from ....transcoder.richchk.richchk_section_transcoder_factory import (
    _RichChkRegistrableTranscoder,
)
from ....transcoder.richchk.transcoders.helpers.richchk_enum_transcoder import (
    RichChkEnumTranscoder,
)

_NUM_FORCES = 4

_RANDOM_START_BIT = 0
_ALLIES_BIT = 1
_ALLIED_VICTORY_BIT = 2
_SHARED_VISION_BIT = 3


class RichForcTranscoder(
    RichChkSectionTranscoder[RichForcSection, DecodedForcSection],
    _RichChkRegistrableTranscoder,
    chk_section_name=DecodedForcSection.section_name(),
):
    def decode(
        self,
        decoded_chk_section: DecodedForcSection,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> RichForcSection:
        forces = [
            RichForce(
                _name=rich_chk_decode_context.rich_str_lookup.get_string_by_id(
                    decoded_chk_section.force_name_string_ids[i]
                ),
                _flags=self._decode_force_flags(decoded_chk_section.force_flags[i]),
            )
            for i in range(_NUM_FORCES)
        ]
        player_force_assignments = [
            RichChkEnumTranscoder.decode_enum(x, ForceId)
            for x in decoded_chk_section.player_force_assignments
        ]
        return RichForcSection(
            _player_force_assignments=player_force_assignments,
            _forces=forces,
        )

    def encode(
        self,
        rich_chk_section: RichForcSection,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedForcSection:
        force_name_string_ids = [
            rich_chk_encode_context.rich_str_lookup.get_id_by_string(force.name)
            for force in rich_chk_section.forces
        ]
        force_flags = [
            self._encode_force_flags(force.flags) for force in rich_chk_section.forces
        ]
        player_force_assignments = [
            RichChkEnumTranscoder.encode_enum(x)
            for x in rich_chk_section.player_force_assignments
        ]
        return DecodedForcSection(
            _player_force_assignments=player_force_assignments,
            _force_name_string_ids=force_name_string_ids,
            _force_flags=force_flags,
        )

    @classmethod
    def _decode_force_flags(cls, flags_byte: int) -> ForceFlags:
        return ForceFlags(
            _random_start=bool(flags_byte & (1 << _RANDOM_START_BIT)),
            _allies=bool(flags_byte & (1 << _ALLIES_BIT)),
            _allied_victory=bool(flags_byte & (1 << _ALLIED_VICTORY_BIT)),
            _shared_vision=bool(flags_byte & (1 << _SHARED_VISION_BIT)),
        )

    @classmethod
    def _encode_force_flags(cls, flags: ForceFlags) -> int:
        result = 0
        if flags.random_start:
            result |= 1 << _RANDOM_START_BIT
        if flags.allies:
            result |= 1 << _ALLIES_BIT
        if flags.allied_victory:
            result |= 1 << _ALLIED_VICTORY_BIT
        if flags.shared_vision:
            result |= 1 << _SHARED_VISION_BIT
        return result
