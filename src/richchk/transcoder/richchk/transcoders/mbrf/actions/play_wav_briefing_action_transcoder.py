from ......model.chk.trig.decoded_trigger_action import DecodedTriggerAction
from ......model.richchk.mbrf.actions.play_wav_briefing_action import (
    PlayWavBriefingAction,
)
from ......model.richchk.richchk_decode_context import RichChkDecodeContext
from ......model.richchk.richchk_encode_context import RichChkEncodeContext
from ......model.richchk.str.rich_string import RichString
from ......util import logger
from ..rich_briefing_action_transcoder import RichBriefingActionTranscoder
from ..rich_briefing_action_transcoder_factory import (
    _RichBriefingActionRegistrableTranscoder,
)


class PlayWavBriefingActionTranscoder(
    RichBriefingActionTranscoder[PlayWavBriefingAction, DecodedTriggerAction],
    _RichBriefingActionRegistrableTranscoder,
    briefing_action_id=PlayWavBriefingAction.action_id(),
):
    def __init__(self) -> None:
        self.log = logger.get_logger(PlayWavBriefingActionTranscoder.__name__)

    def _decode(
        self,
        decoded_action: DecodedTriggerAction,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> PlayWavBriefingAction:
        assert decoded_action.action_id == PlayWavBriefingAction.action_id().id
        return PlayWavBriefingAction(
            _path_to_wav_in_mpq=rich_chk_decode_context.rich_str_lookup.get_string_by_id(
                decoded_action.wav_string_id
            ).value,
            _duration_ms=decoded_action.time,
        )

    def _encode(
        self,
        rich_action: PlayWavBriefingAction,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedTriggerAction:
        duration_ms = self._determine_wav_duration(rich_action, rich_chk_encode_context)
        return DecodedTriggerAction(
            _location_id=0,
            _text_string_id=0,
            _wav_string_id=rich_chk_encode_context.rich_str_lookup.get_id_by_string(
                RichString(_value=rich_action.path_to_wav_in_mpq)
            ),
            _time=duration_ms,
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
        self,
        rich_action: PlayWavBriefingAction,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> int:
        if rich_action.duration_ms is None:
            if not rich_chk_encode_context.wav_metadata_lookup:
                raise ValueError(
                    f"Cannot encode PlayWavBriefing action without wav duration "
                    f"if no metadata exists for action: {rich_action}"
                )
            maybe_metadata = (
                rich_chk_encode_context.wav_metadata_lookup.get_metadata_by_wav_path(
                    rich_action.path_to_wav_in_mpq
                )
            )
            if not maybe_metadata:
                raise ValueError(
                    f"Cannot encode PlayWavBriefing action with undefined duration "
                    f"because no wav metadata was found for action: {rich_action}.  "
                    f"Try adding the WAV file to the MPQ before creating briefings."
                )
            return maybe_metadata.duration_ms
        return rich_action.duration_ms
