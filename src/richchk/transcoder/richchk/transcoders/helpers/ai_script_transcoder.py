import struct

from .....model.richchk.trig.enums.ai_script import (
    AiScript,
    KnownAiScript,
    UnknownAiScript,
)
from .....transcoder.chk.strings_common import _STRING_ENCODING
from .....util import logger


class AiScriptTranscoder:
    _LOG = logger.get_logger("AiScriptTranscoder")
    _AI_SCRIPT_LOOKUP: dict[str, AiScript] = {
        script.value.name: script.value for script in KnownAiScript
    }

    @classmethod
    def _is_known_ai_script(cls, ai_script_name: str) -> bool:
        return ai_script_name in cls._AI_SCRIPT_LOOKUP

    @classmethod
    def decode(cls, ai_script_value: int) -> AiScript:
        # read the U32 value as a 4-byte string
        packed_bytes = struct.pack("I", ai_script_value)
        ai_script_name = packed_bytes.decode(_STRING_ENCODING)
        if not cls._is_known_ai_script(ai_script_name):
            cls._LOG.warning(
                f"Unknown AI script: {ai_script_name} with value {ai_script_value}.  "
                f"Consider adding it to KnownAiScript enum."
            )
            return UnknownAiScript(_name=ai_script_name, _description=ai_script_name)
        maybe_ai_script = cls._AI_SCRIPT_LOOKUP.get(ai_script_name)
        if not maybe_ai_script:
            raise KeyError(
                f"Expected to find a known AI script but found none for AI script name: {ai_script_name}"
            )
        return maybe_ai_script

    @classmethod
    def encode(cls, ai_script: AiScript) -> int:
        # turn the AI script name into a U32
        name_as_bytes = ai_script.name.encode(_STRING_ENCODING)
        value = struct.unpack("I", name_as_bytes)[0]
        assert isinstance(value, int)
        return value
