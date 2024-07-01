"""Decode Leaderboard for showing most unit type controlled at a location."""

from ......model.chk.trig.decoded_trigger_action import DecodedTriggerAction
from ......model.richchk.richchk_decode_context import RichChkDecodeContext
from ......model.richchk.richchk_encode_context import RichChkEncodeContext
from ......model.richchk.trig.actions.leaderboard_show_control_unit_action import (
    LeaderboardShowControlUnitAction,
)
from ......model.richchk.unis.unit_id import UnitId
from ......util import logger
from ...helpers.richchk_enum_transcoder import RichChkEnumTranscoder
from ..rich_trigger_action_transcoder import RichTriggerActionTranscoder
from ..rich_trigger_action_transcoder_factory import (
    _RichTriggerActionRegistrableTranscoder,
)


class RichTriggerLeaderboardShowControlUnitTranscoder(
    RichTriggerActionTranscoder[LeaderboardShowControlUnitAction, DecodedTriggerAction],
    _RichTriggerActionRegistrableTranscoder,
    trigger_action_id=LeaderboardShowControlUnitAction.action_id(),
):
    def __init__(self) -> None:
        self.log = logger.get_logger(
            RichTriggerLeaderboardShowControlUnitTranscoder.__name__
        )

    def _decode(
        self,
        decoded_action: DecodedTriggerAction,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> LeaderboardShowControlUnitAction:
        assert (
            decoded_action.action_id == LeaderboardShowControlUnitAction.action_id().id
        )
        return LeaderboardShowControlUnitAction(
            _text=rich_chk_decode_context.rich_str_lookup.get_string_by_id(
                decoded_action.text_string_id
            ),
            _unit=RichChkEnumTranscoder.decode_enum(
                decoded_action.action_argument_type, UnitId
            ),
        )

    def _encode(
        self,
        rich_action: LeaderboardShowControlUnitAction,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedTriggerAction:
        return DecodedTriggerAction(
            _location_id=0,
            _text_string_id=rich_chk_encode_context.rich_str_lookup.get_id_by_string(
                rich_action.text
            ),
            _wav_string_id=0,
            _time=0,
            _first_group=0,
            _second_group=0,
            _action_argument_type=RichChkEnumTranscoder.encode_enum(rich_action.unit),
            _quantifier_or_switch_or_order=0,
            _action_id=rich_action.action_id().id,
            _flags=0,
            _padding=0,
            _mask_flag=0,
        )
