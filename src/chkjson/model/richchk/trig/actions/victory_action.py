import dataclasses

from ..rich_trigger_action import RichTriggerAction
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class VictoryAction(RichTriggerAction):
    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.VICTORY
