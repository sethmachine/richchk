"""Decode action for showing or hiding computer players in Leaderboards."""

from ......model.chk.trig.decoded_trigger_action import DecodedTriggerAction
from ......model.richchk.richchk_decode_context import RichChkDecodeContext
from ......model.richchk.richchk_encode_context import RichChkEncodeContext
from ......model.richchk.trig.actions.leaderboard_toggle_computers_action import (
    LeaderboardToggleComputersAction,
)
from ......model.richchk.trig.enums.computer_leaderboard_action import (
    ComputerLeaderboardAction,
)
from ......util import logger
from ...helpers.richchk_enum_transcoder import RichChkEnumTranscoder
from ..rich_trigger_action_transcoder import RichTriggerActionTranscoder
from ..rich_trigger_action_transcoder_factory import (
    _RichTriggerActionRegistrableTranscoder,
)


class RichTriggerLeaderboardToggleComputersTranscoder(
    RichTriggerActionTranscoder[LeaderboardToggleComputersAction, DecodedTriggerAction],
    _RichTriggerActionRegistrableTranscoder,
    trigger_action_id=LeaderboardToggleComputersAction.action_id(),
):
    def __init__(self) -> None:
        self.log = logger.get_logger(
            RichTriggerLeaderboardToggleComputersTranscoder.__name__
        )

    def _decode(
        self,
        decoded_action: DecodedTriggerAction,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> LeaderboardToggleComputersAction:
        assert (
            decoded_action.action_id == LeaderboardToggleComputersAction.action_id().id
        )
        return LeaderboardToggleComputersAction(
            _action_state=RichChkEnumTranscoder.decode_enum(
                decoded_action.quantifier_or_switch_or_order, ComputerLeaderboardAction
            )
        )

    def _encode(
        self,
        rich_action: LeaderboardToggleComputersAction,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedTriggerAction:
        return DecodedTriggerAction(
            _location_id=0,
            _text_string_id=0,
            _wav_string_id=0,
            _time=0,
            _first_group=0,
            _second_group=0,
            _action_argument_type=0,
            _quantifier_or_switch_or_order=RichChkEnumTranscoder.encode_enum(
                rich_action.action_state
            ),
            _action_id=rich_action.action_id().id,
            _flags=0,
            _padding=0,
            _mask_flag=0,
        )
