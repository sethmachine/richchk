import struct

from richchk.model.richchk.trig.enums.ai_script import KnownAiScript, UnknownAiScript
from richchk.transcoder.richchk.transcoders.helpers.ai_script_transcoder import (
    AiScriptTranscoder,
)


def test_decodes_and_encodes_known_ai_scripts():
    for known_script in KnownAiScript:
        ai_script_value = AiScriptTranscoder.encode(known_script.value)
        script_again = AiScriptTranscoder.decode(ai_script_value)
        assert AiScriptTranscoder.encode(script_again) == AiScriptTranscoder.encode(
            known_script.value
        )
        assert not isinstance(script_again, UnknownAiScript)


def test_it_decodes_and_encodes_unknown_ai_script():
    unknown_script = "ABCD"
    name_as_bytes = unknown_script.encode("UTF-8")
    value = struct.unpack("I", name_as_bytes)[0]
    script = AiScriptTranscoder.decode(value)
    assert isinstance(script, UnknownAiScript)
    assert AiScriptTranscoder.encode(script) == value
