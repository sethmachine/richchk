import dataclasses
from abc import ABC

from ...mrgn.rich_location import RichLocation
from ...unis.unit_id import UnitId
from ..enums.invincibility import Invincibility
from ..player_id import PlayerId
from ..rich_trigger_action import RichTriggerAction, _RichTriggerActionDefaultsBase
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _SetInvincibilityActionBase(RichTriggerAction, ABC):
    _group: PlayerId
    _unit: UnitId
    _location: RichLocation
    _invincibility: Invincibility

    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.SET_INVINCIBILITY

    @property
    def group(self) -> PlayerId:
        return self._group

    @property
    def unit(self) -> UnitId:
        return self._unit

    @property
    def location(self) -> RichLocation:
        return self._location

    @property
    def invincibility(self) -> Invincibility:
        return self._invincibility


@dataclasses.dataclass(frozen=True)
class SetInvincibilityAction(
    _RichTriggerActionDefaultsBase, _SetInvincibilityActionBase
):
    pass
