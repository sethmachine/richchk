"""Decode the MBRF - Mission Briefings section."""
from typing import Any, ClassVar, Optional, Union, cast

from ....model.chk.mbrf.decoded_mbrf_section import DecodedMbrfSection
from ....model.chk.trig.decoded_player_execution import DecodedPlayerExecution
from ....model.chk.trig.decoded_trigger import DecodedTrigger
from ....model.chk.trig.decoded_trigger_action import DecodedTriggerAction
from ....model.chk.trig.decoded_trigger_condition import DecodedTriggerCondition
from ....model.richchk.mbrf.actions.flags.briefing_action_flags import (
    _DEFAULT_BRIEFING_ACTION_FLAGS,
)
from ....model.richchk.mbrf.briefing_action_id import BriefingActionId
from ....model.richchk.mbrf.rich_briefing import RichBriefing
from ....model.richchk.mbrf.rich_briefing_action import RichBriefingAction
from ....model.richchk.mbrf.rich_mbrf_section import RichMbrfSection
from ....model.richchk.richchk_decode_context import RichChkDecodeContext
from ....model.richchk.richchk_encode_context import RichChkEncodeContext
from ....model.richchk.trig.player_id import PlayerId
from ....transcoder.richchk.richchk_section_transcoder import RichChkSectionTranscoder
from ....transcoder.richchk.richchk_section_transcoder_factory import (
    _RichChkRegistrableTranscoder,
)
from ....util import logger
from .helpers.richchk_enum_transcoder import RichChkEnumTranscoder
from .mbrf.rich_briefing_action_transcoder_factory import (
    RichBriefingActionTranscoderFactory,
)

# The condition byte value that marks the first condition slot in every MBRF entry.
_MBRF_MARKER_CONDITION_ID = 13


class RichChkMbrfTranscoder(
    RichChkSectionTranscoder[RichMbrfSection, DecodedMbrfSection],
    _RichChkRegistrableTranscoder,
    chk_section_name=DecodedMbrfSection.section_name(),
):
    _NUM_CONDITIONS_PER_TRIGGER = 16
    _NUM_ACTIONS_PER_TRIGGER = 64
    _NUM_PLAYER_EXECUTION_IDS = 27

    _action_type_cache: ClassVar[dict[Any, Any]] = {}

    _EMPTY_ACTION: DecodedTriggerAction = DecodedTriggerAction(
        _location_id=0,
        _text_string_id=0,
        _wav_string_id=0,
        _time=0,
        _first_group=0,
        _second_group=0,
        _action_argument_type=0,
        _action_id=BriefingActionId.NO_ACTION.id,
        _quantifier_or_switch_or_order=0,
        _flags=0,
        _padding=0,
        _mask_flag=0,
    )

    _MBRF_MARKER_CONDITION: DecodedTriggerCondition = DecodedTriggerCondition(
        _location_id=0,
        _group=0,
        _quantity=0,
        _unit_id=0,
        _numeric_comparison_operation=0,
        _condition_id=_MBRF_MARKER_CONDITION_ID,
        _numeric_comparand_type=0,
        _flags=0,
        _mask_flag=0,
    )

    _NULL_CONDITION: DecodedTriggerCondition = DecodedTriggerCondition(
        _location_id=0,
        _group=0,
        _quantity=0,
        _unit_id=0,
        _numeric_comparison_operation=0,
        _condition_id=0,
        _numeric_comparand_type=0,
        _flags=0,
        _mask_flag=0,
    )

    def __init__(self) -> None:
        self.log = logger.get_logger(RichChkMbrfTranscoder.__name__)

    def decode(
        self,
        decoded_chk_section: DecodedMbrfSection,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> RichMbrfSection:
        briefings = []
        for trigger in decoded_chk_section.triggers:
            briefings.append(self._decode_briefing(trigger, rich_chk_decode_context))
        return RichMbrfSection(_briefings=briefings)

    def _decode_briefing(
        self,
        decoded_trigger: DecodedTrigger,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> RichBriefing:
        actions = self._decode_actions(decoded_trigger.actions, rich_chk_decode_context)
        players = self._decode_player_execution(decoded_trigger.player_execution)
        return RichBriefing(_actions=actions, _players=players)

    def _decode_actions(
        self,
        decoded_actions: list[DecodedTriggerAction],
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> list[Union[RichBriefingAction, DecodedTriggerAction]]:
        actions: list[Union[RichBriefingAction, DecodedTriggerAction]] = []
        for action in decoded_actions:
            if not RichChkEnumTranscoder.contains_enum_by_id(
                action.action_id, BriefingActionId
            ):
                self.log.error(
                    f"Unknown briefing action ID: {action.action_id}!  "
                    f"Make sure all action bytes are accounted for in the enum."
                )
                actions.append(action)
            else:
                maybe_action = self._decode_single_action(
                    action, rich_chk_decode_context
                )
                if maybe_action:
                    actions.append(maybe_action)
        return actions

    def _decode_single_action(
        self,
        decoded_action: DecodedTriggerAction,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> Optional[Union[RichBriefingAction, DecodedTriggerAction]]:
        action_id = RichChkEnumTranscoder.decode_enum(
            decoded_action.action_id, BriefingActionId
        )
        if action_id != BriefingActionId.NO_ACTION:
            if RichBriefingActionTranscoderFactory.supports_transcoding_briefing_action(
                action_id
            ):
                transcoder = RichBriefingActionTranscoderFactory.make_rich_briefing_action_transcoder(
                    action_id
                )
                return transcoder.decode(decoded_action, rich_chk_decode_context)
            else:
                return decoded_action
        return None

    def _decode_player_execution(
        self, player_execution: DecodedPlayerExecution
    ) -> frozenset[PlayerId]:
        players: set[PlayerId] = set()
        for maybe_player_id, is_used in enumerate(player_execution.player_flags):
            if not RichChkEnumTranscoder.contains_enum_by_id(maybe_player_id, PlayerId):
                msg = f"Missing player ID value in PlayerId enum, got unexpected value: {maybe_player_id}."
                self.log.error(msg)
                raise ValueError(msg)
            player_id = RichChkEnumTranscoder.decode_enum(maybe_player_id, PlayerId)
            if is_used:
                players.add(player_id)
        return frozenset(players)

    def encode(
        self,
        rich_chk_section: RichMbrfSection,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedMbrfSection:
        triggers = []
        for briefing in rich_chk_section.briefings:
            triggers.append(self._encode_briefing(briefing, rich_chk_encode_context))
        return DecodedMbrfSection(_triggers=triggers)

    def _encode_briefing(
        self,
        rich_briefing: RichBriefing,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedTrigger:
        conditions = self._generate_mbrf_conditions()
        actions = self._encode_actions(rich_briefing.actions, rich_chk_encode_context)
        padded_actions = self._pad_actions(actions)
        player_execution = self._encode_player_execution(rich_briefing.players)
        return DecodedTrigger(
            _conditions=conditions,
            _actions=padded_actions,
            _player_execution=player_execution,
        )

    def _pad_actions(
        self, actions: list[DecodedTriggerAction]
    ) -> list[DecodedTriggerAction]:
        padding_needed = self._NUM_ACTIONS_PER_TRIGGER - len(actions)
        if padding_needed < 0:
            raise ValueError(
                f"Too many briefing actions: {len(actions)} exceeds the maximum of "
                f"{self._NUM_ACTIONS_PER_TRIGGER}."
            )
        return actions + [self._EMPTY_ACTION] * padding_needed

    def _generate_mbrf_conditions(self) -> list[DecodedTriggerCondition]:
        # First slot has condition_id=13 (MBRF marker); the remaining 15 are null.
        conditions: list[DecodedTriggerCondition] = [self._MBRF_MARKER_CONDITION]
        conditions += [self._NULL_CONDITION] * (self._NUM_CONDITIONS_PER_TRIGGER - 1)
        return conditions

    def _encode_actions(
        self,
        rich_actions: list[Union[RichBriefingAction, DecodedTriggerAction]],
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> list[DecodedTriggerAction]:
        decoded_actions = []
        cache = RichChkMbrfTranscoder._action_type_cache
        for action in rich_actions:
            action_type = type(action)
            if action_type is DecodedTriggerAction:
                decoded_actions.append(action)
                continue
            rich_action = cast(RichBriefingAction, action)
            transcoder = cache.get(action_type)
            if transcoder is None:
                aid = rich_action.action_id()
                if RichBriefingActionTranscoderFactory.supports_transcoding_briefing_action(
                    aid
                ):
                    transcoder = RichBriefingActionTranscoderFactory.make_rich_briefing_action_transcoder(
                        aid
                    )
                    cache[action_type] = transcoder
                else:
                    msg = (
                        f"Unhandled RichBriefingAction that can't be "
                        f"encoded back due to missing transcoder: {action}"
                    )
                    self.log.error(msg)
                    raise ValueError(msg)
            if rich_action.flags is _DEFAULT_BRIEFING_ACTION_FLAGS:
                decoded_actions.append(
                    transcoder._encode(rich_action, rich_chk_encode_context)
                )
            else:
                decoded_actions.append(
                    transcoder.encode(rich_action, rich_chk_encode_context)
                )
        return cast(list[DecodedTriggerAction], decoded_actions)

    _player_execution_cache: dict[Any, Any] = {}

    def _encode_player_execution(
        self, players: Union[set[PlayerId], frozenset[PlayerId]]
    ) -> DecodedPlayerExecution:
        key = frozenset(players)
        cached = self._player_execution_cache.get(key)
        if cached is not None:
            return cast(DecodedPlayerExecution, cached)
        player_flags = [0] * 27
        for player_id in players:
            player_flags[player_id.id] = 1
        result = DecodedPlayerExecution(
            _execution_flags=0, _player_flags=player_flags, _current_action_index=0
        )
        self._player_execution_cache[key] = result
        return result
