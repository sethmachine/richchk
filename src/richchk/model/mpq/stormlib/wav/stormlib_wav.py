"""Contains metadata about a WAV file stored in an MPQ."""
import dataclasses


@dataclasses.dataclass(frozen=True)
class StormLibWav:
    _path_to_wav_in_mpq: str
    _duration_ms: int

    @property
    def path_to_wav_in_mpq(self) -> str:
        return self._path_to_wav_in_mpq

    @property
    def duration_ms(self) -> int:
        return self._duration_ms
