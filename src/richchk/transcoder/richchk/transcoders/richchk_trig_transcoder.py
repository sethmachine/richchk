"""Decode the TRIG - Triggers section."""
from typing import Any, ClassVar, Optional, Union, cast

from ....model.chk.trig.decoded_player_execution import DecodedPlayerExecution
from ....model.chk.trig.decoded_trig_section import DecodedTrigSection, TrigLazySpec
from ....model.chk.trig.decoded_trigger import DecodedTrigger
from ....model.chk.trig.decoded_trigger_action import DecodedTriggerAction
from ....model.chk.trig.decoded_trigger_condition import DecodedTriggerCondition
from ....model.richchk.richchk_decode_context import RichChkDecodeContext
from ....model.richchk.richchk_encode_context import RichChkEncodeContext
from ....model.richchk.trig.actions.flags.trigger_action_flags import (
    _DEFAULT_TRIGGER_ACTION_FLAGS,
)
from ....model.richchk.trig.conditions.flags.trigger_condition_flags import (
    _DEFAULT_TRIGGER_CONDITION_FLAGS,
)
from ....model.richchk.trig.conditions.no_condition_condition import (
    NoConditionCondition,
)
from ....model.richchk.trig.player_id import PlayerId
from ....model.richchk.trig.rich_trig_section import RichTrigSection
from ....model.richchk.trig.rich_trigger import RichTrigger
from ....model.richchk.trig.rich_trigger_action import RichTriggerAction
from ....model.richchk.trig.rich_trigger_condition import RichTriggerCondition
from ....model.richchk.trig.trigger_action_id import TriggerActionId
from ....model.richchk.trig.trigger_condition_id import TriggerConditionId
from ....transcoder.richchk.richchk_section_transcoder import RichChkSectionTranscoder
from ....transcoder.richchk.richchk_section_transcoder_factory import (
    _RichChkRegistrableTranscoder,
)
from ....util import logger
from .helpers.richchk_enum_transcoder import RichChkEnumTranscoder
from .trig.batched_trig_encode_optimizer import BatchedTrigEncodeOptimizer
from .trig.rich_trigger_action_transcoder_factory import (
    RichTriggerActionTranscoderFactory,
)
from .trig.rich_trigger_condition_transcoder_factory import (
    RichTriggerConditionTranscoderFactory,
)


class RichChkTrigTranscoder(
    RichChkSectionTranscoder[RichTrigSection, DecodedTrigSection],
    _RichChkRegistrableTranscoder,
    chk_section_name=DecodedTrigSection.section_name(),
):

    _action_type_cache: ClassVar[dict[Any, Any]] = {}
    _condition_type_cache: ClassVar[dict[Any, Any]] = {}
    _optimizer: ClassVar[BatchedTrigEncodeOptimizer] = BatchedTrigEncodeOptimizer()

    _EMPTY_ACTION: DecodedTriggerAction = DecodedTriggerAction(
        _location_id=0,
        _text_string_id=0,
        _wav_string_id=0,
        _time=0,
        _first_group=0,
        _second_group=0,
        _action_argument_type=0,
        _action_id=TriggerActionId.NO_ACTION.id,
        _quantifier_or_switch_or_order=0,
        _flags=0,
        _padding=0,
        _mask_flag=0,
    )
    _EMPTY_CONDITION: DecodedTriggerCondition = DecodedTriggerCondition(
        _location_id=0,
        _group=0,
        _quantity=0,
        _unit_id=0,
        _numeric_comparison_operation=0,
        _condition_id=NoConditionCondition.condition_id().id,
        _numeric_comparand_type=0,
        _flags=0,
        _mask_flag=0,
    )

    def __init__(self) -> None:
        self.log = logger.get_logger(RichChkTrigTranscoder.__name__)

    def decode(
        self,
        decoded_chk_section: DecodedTrigSection,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> RichTrigSection:
        rich_triggers = []
        for trigger in decoded_chk_section.triggers:
            rich_triggers.append(self._decode_trigger(trigger, rich_chk_decode_context))
        return RichTrigSection(_triggers=rich_triggers)

    def _decode_trigger(
        self,
        decoded_trigger: DecodedTrigger,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> RichTrigger:
        conditions = self._decode_conditions(
            decoded_trigger.conditions, rich_chk_decode_context
        )
        actions = self._decode_actions(decoded_trigger.actions, rich_chk_decode_context)
        players = self._decode_player_execution(decoded_trigger.player_execution)
        return RichTrigger(_conditions=conditions, _actions=actions, _players=players)

    def _decode_conditions(
        self,
        decoded_conditions: list[DecodedTriggerCondition],
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> list[Union[RichTriggerCondition, DecodedTriggerCondition]]:
        conditions: list[Union[RichTriggerCondition, DecodedTriggerCondition]] = []
        for condition in decoded_conditions:
            if not RichChkEnumTranscoder.contains_enum_by_id(
                condition.condition_id, TriggerConditionId
            ):
                self.log.error(
                    f"Unknown trigger condition ID: {condition.condition_id}!  "
                    f"Make sure all condition bytes are accounted for in the enum."
                )
                conditions.append(condition)
            else:
                maybe_condition = self._decode_single_condition(
                    condition, rich_chk_decode_context
                )
                if maybe_condition:
                    conditions.append(maybe_condition)
        return conditions

    def _decode_single_condition(
        self,
        decoded_condition: DecodedTriggerCondition,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> Optional[Union[RichTriggerCondition, DecodedTriggerCondition]]:
        condition_id = RichChkEnumTranscoder.decode_enum(
            decoded_condition.condition_id, TriggerConditionId
        )
        if condition_id != TriggerConditionId.NO_CONDITION:
            if RichTriggerConditionTranscoderFactory.supports_transcoding_condition(
                condition_id
            ):
                transcoder = RichTriggerConditionTranscoderFactory.make_rich_trigger_condition_transcoder(
                    condition_id
                )
                return transcoder.decode(decoded_condition, rich_chk_decode_context)
            else:
                return decoded_condition
        return None

    def _decode_actions(
        self,
        decoded_actions: list[DecodedTriggerAction],
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> list[Union[RichTriggerAction, DecodedTriggerAction]]:
        actions: list[Union[RichTriggerAction, DecodedTriggerAction]] = []
        for action in decoded_actions:
            if not RichChkEnumTranscoder.contains_enum_by_id(
                action.action_id, TriggerActionId
            ):
                self.log.error(
                    f"Unknown trigger action ID: {action.action_id}!  "
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
    ) -> Optional[Union[RichTriggerAction, DecodedTriggerAction]]:
        action_id = RichChkEnumTranscoder.decode_enum(
            decoded_action.action_id, TriggerActionId
        )
        if action_id != TriggerActionId.NO_ACTION:
            if RichTriggerActionTranscoderFactory.supports_transcoding_trig_action(
                action_id
            ):
                transcoder = RichTriggerActionTranscoderFactory.make_rich_trigger_action_transcoder(
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
        if player_execution.execution_flags != 0:
            msg = (
                f"Unexpected value for trigger execution flags. "
                f"Expected 0 but got {player_execution.execution_flags}"
            )
            self.log.error(msg)
            raise ValueError(msg)
        if player_execution.current_action_index != 0:
            msg = (
                f"Unexpected value for trigger action index. "
                f"Expected 0 but got {player_execution.current_action_index}"
            )
            self.log.error(msg)
            raise ValueError(msg)
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
        rich_chk_section: RichTrigSection,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedTrigSection:
        raw = self._optimizer.encode(rich_chk_section, rich_chk_encode_context)
        if isinstance(raw, TrigLazySpec):
            return DecodedTrigSection(_triggers=[], _lazy_spec=raw)
        return DecodedTrigSection(_triggers=[], _raw_data=raw)

    def get_secondary_cache_key(
        self, rich_chk_section: RichTrigSection
    ) -> Optional[tuple[Any, ...]]:
        return self._optimizer.get_secondary_cache_key(rich_chk_section)

    def _encode_trigger(
        self, rich_trigger: RichTrigger, rich_chk_encode_context: RichChkEncodeContext
    ) -> DecodedTrigger:
        conditions = self._encode_conditions(
            rich_trigger.conditions, rich_chk_encode_context
        )
        actions = self._encode_actions(rich_trigger.actions, rich_chk_encode_context)
        player_execution = self._encode_player_execution(rich_trigger.players)
        return DecodedTrigger(
            _conditions=conditions, _actions=actions, _player_execution=player_execution
        )

    def _encode_conditions(
        self,
        rich_conditions: list[Union[RichTriggerCondition, DecodedTriggerCondition]],
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> list[DecodedTriggerCondition]:
        decoded_conditions = []
        cache = RichChkTrigTranscoder._condition_type_cache
        for condition in rich_conditions:
            condition_type = type(condition)
            if condition_type is DecodedTriggerCondition:
                decoded_conditions.append(condition)
                continue
            rich_condition = cast(RichTriggerCondition, condition)
            transcoder = cache.get(condition_type)
            if transcoder is None:
                cid = rich_condition.condition_id()
                if RichTriggerConditionTranscoderFactory.supports_transcoding_condition(
                    cid
                ):
                    transcoder = RichTriggerConditionTranscoderFactory.make_rich_trigger_condition_transcoder(
                        cid
                    )
                    cache[condition_type] = transcoder
                else:
                    msg = (
                        f"Unhandled RichTriggerCondition that can't be "
                        f"decoded back due to missing transcoder: {condition}"
                    )
                    self.log.error(msg)
                    raise ValueError(msg)
            if rich_condition.flags is _DEFAULT_TRIGGER_CONDITION_FLAGS:
                decoded_conditions.append(
                    transcoder._encode(rich_condition, rich_chk_encode_context)
                )
            else:
                decoded_conditions.append(
                    transcoder.encode(rich_condition, rich_chk_encode_context)
                )
        return cast(list[DecodedTriggerCondition], decoded_conditions)

    def _generate_empty_condition(self) -> DecodedTriggerCondition:
        return self._EMPTY_CONDITION

    def _encode_actions(
        self,
        rich_actions: list[Union[RichTriggerAction, DecodedTriggerAction]],
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> list[DecodedTriggerAction]:
        decoded_actions = []
        cache = RichChkTrigTranscoder._action_type_cache
        for action in rich_actions:
            action_type = type(action)
            if action_type is DecodedTriggerAction:
                decoded_actions.append(action)
                continue
            rich_action = cast(RichTriggerAction, action)
            transcoder = cache.get(action_type)
            if transcoder is None:
                aid = rich_action.action_id()
                if RichTriggerActionTranscoderFactory.supports_transcoding_trig_action(
                    aid
                ):
                    transcoder = RichTriggerActionTranscoderFactory.make_rich_trigger_action_transcoder(
                        aid
                    )
                    cache[action_type] = transcoder
                else:
                    msg = (
                        f"Unhandled RichTriggerAction that can't be "
                        f"decoded back due to missing transcoder: {action}"
                    )
                    self.log.error(msg)
                    raise ValueError(msg)
            if rich_action.flags is _DEFAULT_TRIGGER_ACTION_FLAGS:
                decoded_actions.append(
                    transcoder._encode(rich_action, rich_chk_encode_context)
                )
            else:
                decoded_actions.append(
                    transcoder.encode(rich_action, rich_chk_encode_context)
                )
        return cast(list[DecodedTriggerAction], decoded_actions)

    def _generate_empty_action(self) -> DecodedTriggerAction:
        return self._EMPTY_ACTION

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
