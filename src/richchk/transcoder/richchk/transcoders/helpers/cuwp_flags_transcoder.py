"""Transcode special valid flags, unit property flags, and unit flags for CUWP slots."""
import dataclasses
from typing import Type, TypeVar

from .....model.richchk.uprp.flags.cuwp_flags_base import CuwpFlagsBase

_T = TypeVar("_T", bound=CuwpFlagsBase, covariant=True)


class CuwpFlagsTranscoder:
    @classmethod
    def decode_flags(cls, encoded_flags: int, cuwp_flags_type: Type[_T]) -> _T:
        bit_string_template = f"{{:0{str(cuwp_flags_type.flags_bit_size())}b}}"
        bit_string = bit_string_template.format(encoded_flags)
        num_bits_used_for_flags = len(dataclasses.fields(cuwp_flags_type))
        # Starcraft bit string is read right to left, so the first bit
        # is the last position in the bit string, etc.
        # bit of 1 means the elevation is disabled, 0 is enabled
        decoded_flags = []
        for bit in range(1, num_bits_used_for_flags + 1):
            decoded_flags.append(bool(int(bit_string[bit * -1])))
        return cuwp_flags_type(*decoded_flags)

    @classmethod
    def encode_flags(cls, decoded_flags: CuwpFlagsBase) -> int:
        # encode back each boolean flag in reverse order to get back the original flags value
        encoded_flags = []
        for field in dataclasses.fields(decoded_flags):
            encoded_flags.append(f"{int(getattr(decoded_flags, field.name))}")
        encoded_flags.reverse()

        return int(
            "".join(encoded_flags),
            base=2,
        )
