"""Represents a single mission briefing.

A mission briefing uses the same 2400-byte binary layout as a TRIG trigger. The
conditions block is internal to the format — the first condition slot always has
condition byte 13 to mark it as a briefing; the other 15 are null. This detail is hidden
from the rich model; consumers work only with actions and player ownership.
"""

import dataclasses
from typing import Union

from ...chk.trig.decoded_trigger_action import DecodedTriggerAction
from ..trig.player_id import PlayerId
from .rich_briefing_action import RichBriefingAction


@dataclasses.dataclass(frozen=True, slots=True, init=False)
class RichBriefing:
    """Represents a single mission briefing from the MBRF section.

    :param _actions: Actions of the briefing. Up to 64 action slots, same struct as TRIG
        actions, but using MBRF-specific action IDs (0-9).
    :param _players: The players for which this briefing executes.
    """

    _actions: list[Union[RichBriefingAction, DecodedTriggerAction]]
    _players: frozenset[PlayerId]

    def __init__(
        self,
        _actions: list[Union[RichBriefingAction, DecodedTriggerAction]],
        _players: Union[set[PlayerId], frozenset[PlayerId]],
    ) -> None:
        object.__setattr__(self, "_actions", _actions)
        object.__setattr__(
            self,
            "_players",
            _players if isinstance(_players, frozenset) else frozenset(_players),
        )

    @property
    def actions(self) -> list[Union[RichBriefingAction, DecodedTriggerAction]]:
        return self._actions

    @property
    def players(self) -> frozenset[PlayerId]:
        return self._players
