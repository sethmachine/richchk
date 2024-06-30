"""Decode Run AI script action."""
from ......model.chk.trig.decoded_trigger_action import DecodedTriggerAction
from ......model.richchk.richchk_decode_context import RichChkDecodeContext
from ......model.richchk.richchk_encode_context import RichChkEncodeContext
from ......model.richchk.trig.actions.run_ai_script_action import RunAiScriptAction
from ......util import logger
from ...helpers.ai_script_transcoder import AiScriptTranscoder
from ..rich_trigger_action_transcoder import RichTriggerActionTranscoder
from ..rich_trigger_action_transcoder_factory import (
    _RichTriggerActionRegistrableTranscoder,
)


class RichTriggerRunAiScriptActionTranscoder(
    RichTriggerActionTranscoder[RunAiScriptAction, DecodedTriggerAction],
    _RichTriggerActionRegistrableTranscoder,
    trigger_action_id=RunAiScriptAction.action_id(),
):
    def __init__(self) -> None:
        self.log = logger.get_logger(RichTriggerRunAiScriptActionTranscoder.__name__)

    def _decode(
        self,
        decoded_action: DecodedTriggerAction,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> RunAiScriptAction:
        assert decoded_action.action_id == RunAiScriptAction.action_id().id
        return RunAiScriptAction(
            _ai_script=AiScriptTranscoder.decode(decoded_action.second_group),
        )

    def _encode(
        self,
        rich_action: RunAiScriptAction,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedTriggerAction:
        return DecodedTriggerAction(
            _location_id=0,
            _text_string_id=0,
            _wav_string_id=0,
            _time=0,
            _first_group=0,
            _second_group=AiScriptTranscoder.encode(rich_action.ai_script),
            _action_argument_type=0,
            _action_id=rich_action.action_id().id,
            _quantifier_or_switch_or_order=0,
            _flags=0,
            _padding=0,
            _mask_flag=0,
        )
