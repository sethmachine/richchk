"""Read and write CHK data.

The CHK is split into several named chunks (hence the file extension, an abbreviation of CHunK).

Each section begins with an 8-byte header:

u32 Name - A 4-byte string uniquely identifying that chunk's purpose.
u32 Size - The size, in bytes, of the chunk (not including this header)
Followed by as many bytes as 'Size', in a format described below.

Some things to keep in mind about the CHK section:

Invalid sections can exist and will be ignored. While Size is unsigned, it can safely be a negative value to read a chunk earlier in the file. This allows for "section stacking", allowing smaller sections to be placed inside of larger ones or duplicate triggers or units to take less space in the file.
All sections will marked "Not required." are never read by StarCraft and can safely be omitted. However they may or may not be read by StarEdit, and may cause the map to be unreadable in an editor.
Note "Hybrid", or "Enhanced", maps were introduced in 1.04. They are supported both by Original StarCraft and Brood War and usually contain sections for both types (e.g., UPGS and UPGx, TECS and TECx), but both sections aren't necessarily read.
Duplicate sections will overwrite previously defined section data, except where noted. Note this only applies to those section that pass the specified "validation" parameters, as any section that does not successfully validate will be ignored

"""

import struct
from io import BytesIO
from typing import Protocol

from ..model.chk.decoded_chk import DecodedChk
from ..model.chk.decoded_chk_section import DecodedChkSection
from ..model.chk.unknown.decoded_unknown_section import DecodedUnknownSection
from ..model.chk_section_name import ChkSectionName
from ..transcoder.chk_section_transcoder import ChkSectionTranscoder
from ..transcoder.chk_section_transcoder_factory import ChkSectionTranscoderFactory
from ..util import logger

_CHK_SECTION_NAME_NUM_BYTES: int = 4
_CHK_SECTION_TOTAL_BYTES_NUM_BYTES: int = 4


class _ByteStream(Protocol):
    def read(self, num_bytes: int) -> bytes:
        raise NotImplementedError


class ChkIo:
    def __init__(self):
        self.log = logger.get_logger(ChkIo.__name__)

    def decode_chk_file(self, chk_file_path: str) -> DecodedChk:
        with open(chk_file_path, "rb") as f:
            return self._decode_chk_byte_stream(f)

    def decode_chk_binary_data(self, chk_binary_data: bytes) -> DecodedChk:
        return self._decode_chk_byte_stream(BytesIO(chk_binary_data))

    def encode_chk_to_file(
        self, decoded_chk: DecodedChk, chk_output_file_path: str
    ) -> None:
        pass

    def encode_chk_to_bytes(self, decoded_chk: DecodedChk) -> bytes:
        pass

    def _decode_chk_byte_stream(self, chk_byte_stream: _ByteStream) -> DecodedChk:
        decoded_chk_sections: list[DecodedChkSection] = []
        maybe_chk_section_name_bytes = chk_byte_stream.read(_CHK_SECTION_NAME_NUM_BYTES)
        while maybe_chk_section_name_bytes != b"":
            # u32 Name - A 4-byte string uniquely identifying that chunk's purpose.
            maybe_chk_section_name = struct.unpack("4s", maybe_chk_section_name_bytes)[
                0
            ].decode("utf-8")
            # u32 Size - The size, in bytes, of the chunk (not including this header)
            chk_section_size_in_bytes = struct.unpack(
                "I", chk_byte_stream.read(_CHK_SECTION_TOTAL_BYTES_NUM_BYTES)
            )[0]
            decoded_chk_sections.append(
                self._decode_chk_binary_data_to_chk_section(
                    maybe_chk_section_name,
                    chk_byte_stream.read(chk_section_size_in_bytes),
                )
            )
            # get next CHK section name if it exists
            maybe_chk_section_name_bytes = chk_byte_stream.read(
                _CHK_SECTION_NAME_NUM_BYTES
            )
        return DecodedChk(decoded_chk_sections)

    def _decode_chk_binary_data_to_chk_section(
        self, maybe_chk_section_name: str, chk_section_binary_data: bytes
    ) -> DecodedChkSection:
        if not ChkSectionName.contains(maybe_chk_section_name):
            self.log.warn(
                f"Unknown CHK section name not found in ChkSectionName enum: "
                f"{maybe_chk_section_name}.  "
                f"Will decode as unknown section."
            )
            return self._decode_unknown_chk_section(
                maybe_chk_section_name, chk_section_binary_data
            )
        chk_section_name: ChkSectionName = ChkSectionName.get_by_value(
            maybe_chk_section_name
        )
        if chk_section_name.value == "STR ":
            print("Hi")
        try:
            transcoder: ChkSectionTranscoder = (
                ChkSectionTranscoderFactory.make_chk_section_transcoder(
                    chk_section_name
                )
            )
            return transcoder.decode(chk_section_binary_data)
        except NotImplementedError:
            self.log.error(
                f"CHK section name is available as enum but not registered "
                f"as a transcoder: {maybe_chk_section_name}.  "
                f"Will decode as unknown section."
            )
            return self._decode_unknown_chk_section(
                maybe_chk_section_name, chk_section_binary_data
            )

    @classmethod
    def _decode_unknown_chk_section(
        cls, unknown_chk_section_name: str, chk_section_binary_data: bytes
    ) -> DecodedUnknownSection:
        return DecodedUnknownSection(unknown_chk_section_name, chk_section_binary_data)
