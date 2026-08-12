"""Decode and encode the SPRP - Scenario Properties section."""
import struct
from io import BytesIO

from ....model.chk.sprp.decoded_sprp_section import DecodedSprpSection
from ....transcoder.chk.chk_section_transcoder import ChkSectionTranscoder
from ....transcoder.chk.chk_section_transcoder_factory import _RegistrableTranscoder


class ChkSprpTranscoder(
    ChkSectionTranscoder[DecodedSprpSection],
    _RegistrableTranscoder,
    chk_section_name=DecodedSprpSection.section_name(),
):
    def decode(self, chk_section_binary_data: bytes) -> DecodedSprpSection:
        bytes_stream: BytesIO = BytesIO(chk_section_binary_data)
        scenario_name_string_id = struct.unpack("H", bytes_stream.read(2))[0]
        scenario_description_string_id = struct.unpack("H", bytes_stream.read(2))[0]
        return DecodedSprpSection(
            _scenario_name_string_id=scenario_name_string_id,
            _scenario_description_string_id=scenario_description_string_id,
        )

    def _encode(self, decoded_chk_section: DecodedSprpSection) -> bytes:
        data: bytes = b""
        data += struct.pack("H", decoded_chk_section.scenario_name_string_id)
        data += struct.pack("H", decoded_chk_section.scenario_description_string_id)
        return data
