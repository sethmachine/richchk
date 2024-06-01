from typing import Generic, Type, TypeVar

from .....model.richchk.richchk_enum import RichChkEnum
from .....util import logger

_T = TypeVar("_T", bound=RichChkEnum, covariant=True)


class RichChkEnumTranscoder(Generic[_T]):
    _LOG = logger.get_logger("RichChkEnumTranscoder")
    _ENUM_ID_MAP: dict[Type[_T], dict[int, _T]] = {}

    @classmethod
    def _update_enum_id_map(cls, enum_type: Type[_T]) -> None:
        if enum_type not in cls._ENUM_ID_MAP:
            cls._ENUM_ID_MAP[enum_type] = {}
            for enum_instance in enum_type:
                cls._ENUM_ID_MAP[enum_type][enum_instance.id] = enum_instance

    @classmethod
    def contains_enum_by_id(cls, maybe_enum_id: int, enum_type: Type[_T]) -> bool:
        cls._update_enum_id_map(enum_type)
        try:
            return maybe_enum_id in cls._ENUM_ID_MAP[enum_type]
        except KeyError:
            return False

    @classmethod
    def _get_enum_by_id(cls, maybe_enum_id: int, enum_type: Type[_T]) -> _T:
        try:
            enum_instance = cls._ENUM_ID_MAP[enum_type][maybe_enum_id]
            assert isinstance(enum_instance, enum_type)
            return enum_instance
        except KeyError:
            msg = (
                f"Unexpected enum ID: {maybe_enum_id} for enum {enum_type}.  "
                f"Expected one of {[x for x in enum_type]}"
            )
            cls._LOG.error(msg)
            raise KeyError(msg)

    @classmethod
    def decode_enum(cls, maybe_enum_id: int, enum_type: Type[_T]) -> _T:
        cls._update_enum_id_map(enum_type)
        if not cls.contains_enum_by_id(maybe_enum_id, enum_type):
            msg = (
                f"Unexpected enum ID: {maybe_enum_id} for enum {enum_type}.  "
                f"Expected one of {[x for x in enum_type]}"
            )
            cls._LOG.error(msg)
            raise KeyError(msg)
        return cls._get_enum_by_id(maybe_enum_id, enum_type)

    @classmethod
    def encode_enum(cls, rich_enum: RichChkEnum) -> int:
        return rich_enum.id
