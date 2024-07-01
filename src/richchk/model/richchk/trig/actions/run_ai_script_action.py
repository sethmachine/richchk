import dataclasses
from abc import ABC

from ..enums.ai_script import AiScript
from ..rich_trigger_action import RichTriggerAction, _RichTriggerActionDefaultsBase
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _RunAiScriptActionBase(RichTriggerAction, ABC):
    _ai_script: AiScript

    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.RUN_AI_SCRIPT

    @property
    def ai_script(self) -> AiScript:
        return self._ai_script


@dataclasses.dataclass(frozen=True)
class RunAiScriptAction(_RichTriggerActionDefaultsBase, _RunAiScriptActionBase):
    pass
