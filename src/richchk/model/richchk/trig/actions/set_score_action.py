import dataclasses
from abc import ABC

from ..enums.amount_modifier import AmountModifier
from ..enums.score_type import ScoreType
from ..player_id import PlayerId
from ..rich_trigger_action import RichTriggerAction, _RichTriggerActionDefaultsBase
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _SetScoreActionBase(RichTriggerAction, ABC):
    _group: PlayerId
    _amount_modifier: AmountModifier
    _amount: int
    _score_type: ScoreType

    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.SET_SCORE

    @property
    def group(self) -> PlayerId:
        return self._group

    @property
    def amount(self) -> int:
        return self._amount

    @property
    def amount_modifier(self) -> AmountModifier:
        return self._amount_modifier

    @property
    def score_type(self) -> ScoreType:
        return self._score_type


@dataclasses.dataclass(frozen=True)
class SetScoreAction(_RichTriggerActionDefaultsBase, _SetScoreActionBase):
    pass
