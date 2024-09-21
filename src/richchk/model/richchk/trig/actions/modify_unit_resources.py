import dataclasses
from abc import ABC

from ...mrgn.rich_location import RichLocation
from ...unis.unit_id import UnitId
from ..player_id import PlayerId
from ..rich_trigger_action import RichTriggerAction, _RichTriggerActionDefaultsBase
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _ModifyUnitResourcesActionBase(RichTriggerAction, ABC):
    _group: PlayerId
    _unit: UnitId
    _amount: int
    _resource_amount: int
    _location: RichLocation

    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.MODIFY_UNIT_RESOURCE_AMOUNT

    @property
    def group(self) -> PlayerId:
        return self._group

    @property
    def unit(self) -> UnitId:
        return self._unit

    @property
    def amount(self) -> int:
        return self._amount

    @property
    def resource_amount(self) -> int:
        return self._resource_amount

    @property
    def location(self) -> RichLocation:
        return self._location


@dataclasses.dataclass(frozen=True)
class ModifyUnitResourcesAction(
    _RichTriggerActionDefaultsBase, _ModifyUnitResourcesActionBase
):
    pass
