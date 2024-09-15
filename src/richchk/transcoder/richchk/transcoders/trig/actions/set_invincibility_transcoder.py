"""Decode Set unit invincibility trigger action."""

from ......model.chk.trig.decoded_trigger_action import DecodedTriggerAction
from ......model.richchk.mrgn.rich_location import RichLocation
from ......model.richchk.richchk_decode_context import RichChkDecodeContext
from ......model.richchk.richchk_encode_context import RichChkEncodeContext
from ......model.richchk.trig.actions.set_invincibility_action import (
    SetInvincibilityAction,
)
from ......model.richchk.trig.enums.invincibility import Invincibility
from ......model.richchk.trig.player_id import PlayerId
from ......model.richchk.unis.unit_id import UnitId
from ......util import logger
from ...helpers.richchk_enum_transcoder import RichChkEnumTranscoder
from ..rich_trigger_action_transcoder import RichTriggerActionTranscoder
from ..rich_trigger_action_transcoder_factory import (
    _RichTriggerActionRegistrableTranscoder,
)


class RichTriggerSetInvincibilityActionTranscoder(
    RichTriggerActionTranscoder[SetInvincibilityAction, DecodedTriggerAction],
    _RichTriggerActionRegistrableTranscoder,
    trigger_action_id=SetInvincibilityAction.action_id(),
):
    def __init__(self) -> None:
        self.log = logger.get_logger(
            RichTriggerSetInvincibilityActionTranscoder.__name__
        )

    def _decode(
        self,
        decoded_action: DecodedTriggerAction,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> SetInvincibilityAction:
        assert decoded_action.action_id == SetInvincibilityAction.action_id().id
        assert rich_chk_decode_context.rich_mrgn_lookup is not None
        maybe_location = rich_chk_decode_context.rich_mrgn_lookup.get_location_by_id(
            decoded_action.location_id
        )
        assert isinstance(maybe_location, RichLocation)
        return SetInvincibilityAction(
            _group=RichChkEnumTranscoder.decode_enum(
                decoded_action.first_group, PlayerId
            ),
            _unit=RichChkEnumTranscoder.decode_enum(
                decoded_action.action_argument_type, UnitId
            ),
            _location=maybe_location,
            _invincibility=RichChkEnumTranscoder.decode_enum(
                decoded_action.quantifier_or_switch_or_order, Invincibility
            ),
        )

    def _encode(
        self,
        rich_action: SetInvincibilityAction,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedTriggerAction:
        assert rich_chk_encode_context.rich_mrgn_lookup is not None
        maybe_location_id = rich_chk_encode_context.rich_mrgn_lookup.get_id_by_location(
            rich_action.location
        )
        assert maybe_location_id is not None
        return DecodedTriggerAction(
            _location_id=maybe_location_id,
            _text_string_id=0,
            _wav_string_id=0,
            _time=0,
            _first_group=RichChkEnumTranscoder.encode_enum(rich_action.group),
            _second_group=0,
            _action_argument_type=RichChkEnumTranscoder.encode_enum(rich_action.unit),
            _action_id=rich_action.action_id().id,
            _quantifier_or_switch_or_order=RichChkEnumTranscoder.encode_enum(
                rich_action.invincibility
            ),
            _flags=0,
            _padding=0,
            _mask_flag=0,
        )
