"""Decode Leaderboard for showing most unit type controlled at a location."""

from ......model.chk.trig.decoded_trigger_action import DecodedTriggerAction
from ......model.richchk.richchk_decode_context import RichChkDecodeContext
from ......model.richchk.richchk_encode_context import RichChkEncodeContext
from ......model.richchk.trig.actions.leaderboard_goal_greed_action import (
    LeaderboardGoalGreedAction,
)
from ......util import logger
from ..rich_trigger_action_transcoder import RichTriggerActionTranscoder
from ..rich_trigger_action_transcoder_factory import (
    _RichTriggerActionRegistrableTranscoder,
)


class RichTriggerLeaderboardGoalGreedTranscoder(
    RichTriggerActionTranscoder[LeaderboardGoalGreedAction, DecodedTriggerAction],
    _RichTriggerActionRegistrableTranscoder,
    trigger_action_id=LeaderboardGoalGreedAction.action_id(),
):
    def __init__(self) -> None:
        self.log = logger.get_logger(RichTriggerLeaderboardGoalGreedTranscoder.__name__)

    def _decode(
        self,
        decoded_action: DecodedTriggerAction,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> LeaderboardGoalGreedAction:
        assert decoded_action.action_id == LeaderboardGoalGreedAction.action_id().id
        return LeaderboardGoalGreedAction(
            _goal=decoded_action.second_group,
        )

    def _encode(
        self,
        rich_action: LeaderboardGoalGreedAction,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedTriggerAction:
        return DecodedTriggerAction(
            _location_id=0,
            _text_string_id=0,
            _wav_string_id=0,
            _time=0,
            _first_group=0,
            _second_group=rich_action.goal,
            _action_argument_type=0,
            _quantifier_or_switch_or_order=0,
            _action_id=rich_action.action_id().id,
            _flags=0,
            _padding=0,
            _mask_flag=0,
        )
