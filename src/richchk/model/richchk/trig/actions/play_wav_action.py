import dataclasses
from abc import ABC
from typing import Optional

from ..rich_trigger_action import RichTriggerAction, _RichTriggerActionDefaultsBase
from ..trigger_action_id import TriggerActionId


@dataclasses.dataclass(frozen=True)
class _PlayWavActionBase(RichTriggerAction, ABC):
    _path_to_wav_in_mpq: str
    _duration_ms: Optional[int] = None

    @classmethod
    def action_id(cls) -> TriggerActionId:
        return TriggerActionId.PLAY_WAV

    @property
    def path_to_wav_in_mpq(self) -> str:
        return self._path_to_wav_in_mpq

    @property
    def duration_ms(self) -> Optional[int]:
        return self._duration_ms


@dataclasses.dataclass(frozen=True)
class PlayWavAction(_RichTriggerActionDefaultsBase, _PlayWavActionBase):
    pass
