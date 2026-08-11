import dataclasses
from abc import ABC
from typing import Optional

from ..briefing_action_id import BriefingActionId
from ..rich_briefing_action import RichBriefingAction, _RichBriefingActionDefaultsBase


@dataclasses.dataclass(frozen=True)
class _PlayWavBriefingActionBase(RichBriefingAction, ABC):
    _path_to_wav_in_mpq: str
    _duration_ms: Optional[int] = None

    @classmethod
    def action_id(cls) -> BriefingActionId:
        return BriefingActionId.PLAY_WAV

    @property
    def path_to_wav_in_mpq(self) -> str:
        return self._path_to_wav_in_mpq

    @property
    def duration_ms(self) -> Optional[int]:
        return self._duration_ms


@dataclasses.dataclass(frozen=True)
class PlayWavBriefingAction(
    _RichBriefingActionDefaultsBase, _PlayWavBriefingActionBase
):
    pass
