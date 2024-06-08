import dataclasses
from abc import ABC

from ...str.rich_string import RichString
from ..rich_trigger_action import RichTriggerAction, _RichTriggerActionDefaultsBase
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _DisplayTextMessageActionBase(RichTriggerAction, ABC):
    _text: RichString

    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.DISPLAY_TEXT_MESSAGE

    @property
    def message(self) -> RichString:
        return self._text


@dataclasses.dataclass(frozen=True)
class DisplayTextMessageAction(
    _RichTriggerActionDefaultsBase, _DisplayTextMessageActionBase
):
    pass
