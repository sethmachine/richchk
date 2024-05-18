from typing import Type, TypeVar

from chkjson.model.richchk.richchk_enum import RichChkEnum
from chkjson.util import logger

_T = TypeVar("_T", bound=RichChkEnum, covariant=True)


class RichChkEnumTranscoder:
    _LOG = logger.get_logger("RichChkEnumTranscoder")

    @classmethod
    def decode_enum(cls, maybe_enum_id: int, enum_type: Type[_T]) -> _T:
        msg = (
            f"Unexpected enum ID: {maybe_enum_id} for enum {enum_type}.  "
            f"Expected one of {[x for x in enum_type]}"
        )
        if not enum_type.contains(maybe_enum_id):
            cls._LOG.error(msg)
            raise ValueError(msg)
        rich_enum = enum_type.get_by_id(maybe_enum_id)
        # this next step is required to do the "type casting"
        for val in enum_type:
            if val == rich_enum:
                return val
        # this should be impossible to reach but left to silence warnings about no return statement
        cls._LOG.critical("Impossible to reach error!: " + msg)
        raise ValueError(msg)

    @classmethod
    def encode_enum(cls, rich_enum: RichChkEnum) -> int:
        return rich_enum.id
