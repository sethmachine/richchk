import dataclasses
from abc import ABC

from ..enums.computer_leaderboard_action import ComputerLeaderboardAction
from ..rich_trigger_action import RichTriggerAction, _RichTriggerActionDefaultsBase
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _LeaderboardToggleComputersActionBase(RichTriggerAction, ABC):
    _action_state: ComputerLeaderboardAction

    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.LEADERBOARD_COMPUTER_PLAYERS

    @property
    def action_state(self) -> ComputerLeaderboardAction:
        return self._action_state


@dataclasses.dataclass(frozen=True)
class LeaderboardToggleComputersAction(
    _RichTriggerActionDefaultsBase, _LeaderboardToggleComputersActionBase
):
    pass
