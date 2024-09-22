import dataclasses
from abc import ABC

from ..enums.alliance_status import AllianceStatus
from ..player_id import PlayerId
from ..rich_trigger_action import RichTriggerAction, _RichTriggerActionDefaultsBase
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _SetAllianceStatusActionBase(RichTriggerAction, ABC):
    _group: PlayerId
    _alliance_status: AllianceStatus

    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.SET_ALLIANCE_STATUS

    @property
    def group(self) -> PlayerId:
        return self._group

    @property
    def alliance_status(self) -> AllianceStatus:
        return self._alliance_status


@dataclasses.dataclass(frozen=True)
class SetAllianceStatusAction(
    _RichTriggerActionDefaultsBase, _SetAllianceStatusActionBase
):
    pass
