"""Decode Play WAV file action."""

from ......model.chk.trig.decoded_trigger_action import DecodedTriggerAction
from ......model.richchk.richchk_decode_context import RichChkDecodeContext
from ......model.richchk.richchk_encode_context import RichChkEncodeContext
from ......model.richchk.str.rich_string import RichString
from ......model.richchk.trig.actions.play_wav_action import PlayWavAction
from ......util import logger
from ..rich_trigger_action_transcoder import RichTriggerActionTranscoder
from ..rich_trigger_action_transcoder_factory import (
    _RichTriggerActionRegistrableTranscoder,
)


class RichTriggerPlayWavActionTranscoder(
    RichTriggerActionTranscoder[PlayWavAction, DecodedTriggerAction],
    _RichTriggerActionRegistrableTranscoder,
    trigger_action_id=PlayWavAction.action_id(),
):
    def __init__(self) -> None:
        self.log = logger.get_logger(RichTriggerPlayWavActionTranscoder.__name__)

    def _decode(
        self,
        decoded_action: DecodedTriggerAction,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> PlayWavAction:
        assert decoded_action.action_id == PlayWavAction.action_id().id
        return PlayWavAction(
            _path_to_wav_in_mpq=rich_chk_decode_context.rich_str_lookup.get_string_by_id(
                decoded_action.wav_string_id
            ).value,
            _duration_ms=decoded_action.time,
        )

    def _encode(
        self,
        rich_action: PlayWavAction,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedTriggerAction:
        return DecodedTriggerAction(
            _location_id=0,
            _text_string_id=0,
            _wav_string_id=rich_chk_encode_context.rich_str_lookup.get_id_by_string(
                RichString(_value=rich_action.path_to_wav_in_mpq)
            ),
            _time=self._determine_wav_duration(rich_action, rich_chk_encode_context),
            _first_group=0,
            _second_group=0,
            _action_argument_type=0,
            _action_id=rich_action.action_id().id,
            _quantifier_or_switch_or_order=0,
            _flags=0,
            _padding=0,
            _mask_flag=0,
        )

    def _determine_wav_duration(
        self, rich_action: PlayWavAction, rich_chk_encode_context: RichChkEncodeContext
    ) -> int:
        if rich_action.duration_ms is None:
            if not rich_chk_encode_context.wav_metadata_lookup:
                raise ValueError(
                    f"Cannot encode PlayWav action without corresponding wav file duration "
                    f"if no duration is specified and no metadata exists for action: {rich_action}"
                )
            maybe_metadata = (
                rich_chk_encode_context.wav_metadata_lookup.get_metadata_by_wav_path(
                    rich_action.path_to_wav_in_mpq
                )
            )
            if not maybe_metadata:
                raise ValueError(
                    f"Cannot encode PlayWav Action with undefined duration "
                    f"because no wav metadata was found for action: {rich_action}.  "
                    f"Try adding the WAV file to the MPQ before creating triggers."
                )
            return maybe_metadata.duration_ms
        else:
            return rich_action.duration_ms
