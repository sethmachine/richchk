import abc
import dataclasses


@dataclasses.dataclass(frozen=True)
class CuwpFlagsBase(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def flags_bit_size(cls) -> int:
        pass
