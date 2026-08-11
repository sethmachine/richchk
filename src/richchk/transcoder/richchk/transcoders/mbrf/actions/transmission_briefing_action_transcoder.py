from typing import Optional

from ......model.chk.trig.decoded_trigger_action import DecodedTriggerAction
from ......model.richchk.mbrf.actions.transmission_briefing_action import (
    TransmissionBriefingAction,
)
from ......model.richchk.richchk_decode_context import RichChkDecodeContext
from ......model.richchk.richchk_encode_context import RichChkEncodeContext
from ......model.richchk.str.rich_string import RichString
from ......util import logger
from ..rich_briefing_action_transcoder import RichBriefingActionTranscoder
from ..rich_briefing_action_transcoder_factory import (
    _RichBriefingActionRegistrableTranscoder,
)


class TransmissionBriefingActionTranscoder(
    RichBriefingActionTranscoder[TransmissionBriefingAction, DecodedTriggerAction],
    _RichBriefingActionRegistrableTranscoder,
    briefing_action_id=TransmissionBriefingAction.action_id(),
):
    def __init__(self) -> None:
        self.log = logger.get_logger(TransmissionBriefingActionTranscoder.__name__)

    def _decode(
        self,
        decoded_action: DecodedTriggerAction,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> TransmissionBriefingAction:
        assert decoded_action.action_id == TransmissionBriefingAction.action_id().id
        maybe_wav: Optional[str] = None
        if decoded_action.wav_string_id:
            maybe_wav = rich_chk_decode_context.rich_str_lookup.get_string_by_id(
                decoded_action.wav_string_id
            ).value
        return TransmissionBriefingAction(
            _text=rich_chk_decode_context.rich_str_lookup.get_string_by_id(
                decoded_action.text_string_id
            ),
            _slot=decoded_action.first_group,
            _duration_ms=decoded_action.time,
            _path_to_wav_in_mpq=maybe_wav,
            _wav_duration_ms=decoded_action.second_group
            if decoded_action.second_group
            else None,
        )

    def _encode(
        self,
        rich_action: TransmissionBriefingAction,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedTriggerAction:
        wav_string_id = 0
        if rich_action.path_to_wav_in_mpq:
            wav_string_id = rich_chk_encode_context.rich_str_lookup.get_id_by_string(
                RichString(_value=rich_action.path_to_wav_in_mpq)
            )
        wav_duration_ms = self._determine_wav_duration(
            rich_action, rich_chk_encode_context
        )
        return DecodedTriggerAction(
            _location_id=0,
            _text_string_id=rich_chk_encode_context.rich_str_lookup.get_id_by_string(
                rich_action.message
            ),
            _wav_string_id=wav_string_id,
            _time=rich_action.duration_ms,
            _first_group=rich_action.slot,
            _second_group=wav_duration_ms,
            _action_argument_type=0,
            _action_id=rich_action.action_id().id,
            _quantifier_or_switch_or_order=0,
            _flags=0,
            _padding=0,
            _mask_flag=0,
        )

    def _determine_wav_duration(
        self,
        rich_action: TransmissionBriefingAction,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> int:
        if rich_action.wav_duration_ms is not None:
            return rich_action.wav_duration_ms
        if (
            rich_action.path_to_wav_in_mpq
            and rich_chk_encode_context.wav_metadata_lookup
        ):
            maybe_metadata = (
                rich_chk_encode_context.wav_metadata_lookup.get_metadata_by_wav_path(
                    rich_action.path_to_wav_in_mpq
                )
            )
            if maybe_metadata:
                return maybe_metadata.duration_ms
        return 0
