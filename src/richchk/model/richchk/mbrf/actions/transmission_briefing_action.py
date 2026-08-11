import dataclasses
from abc import ABC
from typing import Optional

from ...str.rich_string import RichString
from ..briefing_action_id import BriefingActionId
from ..rich_briefing_action import RichBriefingAction, _RichBriefingActionDefaultsBase


@dataclasses.dataclass(frozen=True)
class _TransmissionBriefingActionBase(RichBriefingAction, ABC):
    _text: RichString
    _slot: int
    _duration_ms: int
    _path_to_wav_in_mpq: Optional[str] = None
    _wav_duration_ms: Optional[int] = None

    @classmethod
    def action_id(cls) -> BriefingActionId:
        return BriefingActionId.TRANSMISSION

    @property
    def message(self) -> RichString:
        return self._text

    @property
    def slot(self) -> int:
        return self._slot

    @property
    def duration_ms(self) -> int:
        return self._duration_ms

    @property
    def path_to_wav_in_mpq(self) -> Optional[str]:
        return self._path_to_wav_in_mpq

    @property
    def wav_duration_ms(self) -> Optional[int]:
        return self._wav_duration_ms


@dataclasses.dataclass(frozen=True)
class TransmissionBriefingAction(
    _RichBriefingActionDefaultsBase, _TransmissionBriefingActionBase
):
    pass
