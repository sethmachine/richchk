import dataclasses

from ...mrgn.rich_location import RichLocation
from ...unis.unit_id import UnitId
from ..player_id import PlayerId
from ..rich_trigger_action import RichTriggerAction
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class CreateUnitAction(RichTriggerAction):
    for_player: PlayerId
    amount: int
    unit_id: UnitId
    location: RichLocation

    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.CREATE_UNIT
