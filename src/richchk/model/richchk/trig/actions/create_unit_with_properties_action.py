import dataclasses
from abc import ABC

from ...mrgn.rich_location import RichLocation
from ...unis.unit_id import UnitId
from ...uprp.rich_cuwp_slot import RichCuwpSlot
from ..player_id import PlayerId
from ..rich_trigger_action import RichTriggerAction, _RichTriggerActionDefaultsBase
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _CreateUnitWithPropertiesActionBase(RichTriggerAction, ABC):
    _group: PlayerId
    _amount: int
    _unit: UnitId
    _location: RichLocation
    _properties: RichCuwpSlot

    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.CREATE_UNIT_WITH_PROPERTIES

    @property
    def group(self) -> PlayerId:
        return self._group

    @property
    def amount(self) -> int:
        return self._amount

    @property
    def unit(self) -> UnitId:
        return self._unit

    @property
    def location(self) -> RichLocation:
        return self._location

    @property
    def properties(self) -> RichCuwpSlot:
        return self._properties


@dataclasses.dataclass(frozen=True)
class CreateUnitWithPropertiesAction(
    _RichTriggerActionDefaultsBase, _CreateUnitWithPropertiesActionBase
):
    pass
