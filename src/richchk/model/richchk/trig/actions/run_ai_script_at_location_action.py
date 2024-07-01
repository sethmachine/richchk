import dataclasses
from abc import ABC

from ...mrgn.rich_location import RichLocation
from ..enums.ai_script import AiScript
from ..rich_trigger_action import RichTriggerAction, _RichTriggerActionDefaultsBase
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _RunAiScriptAtLocationActionBase(RichTriggerAction, ABC):
    _ai_script: AiScript
    _location: RichLocation

    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.RUN_AI_SCRIPT_AT_LOCATION

    @property
    def ai_script(self) -> AiScript:
        return self._ai_script

    @property
    def location(self) -> RichLocation:
        return self._location


@dataclasses.dataclass(frozen=True)
class RunAiScriptAtLocationAction(
    _RichTriggerActionDefaultsBase, _RunAiScriptAtLocationActionBase
):
    pass
