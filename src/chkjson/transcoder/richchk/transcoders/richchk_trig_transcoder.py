"""Decode the TRIG - Triggers section."""
from typing import Union

from ....model.chk.trig.decoded_player_execution import DecodedPlayerExecution
from ....model.chk.trig.decoded_trig_section import DecodedTrigSection
from ....model.chk.trig.decoded_trigger import DecodedTrigger
from ....model.chk.trig.decoded_trigger_action import DecodedTriggerAction
from ....model.chk.trig.decoded_trigger_condition import DecodedTriggerCondition
from ....model.richchk.richchk_decode_context import RichChkDecodeContext
from ....model.richchk.richchk_encode_context import RichChkEncodeContext
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
            if not TriggerConditionId.contains(condition.condition_id):
                self.log.error(
                    f"Unknown trigger condition ID: {condition.condition_id}!  "
                    f"Make sure all condition bytes are accounted for in the enum."
                )
                conditions.append(condition)
            else:
                condition_id = TriggerConditionId.get_by_id(condition.condition_id)
                if RichTriggerConditionTranscoderFactory.supports_transcoding_trig_action(
                    condition_id
                ):
                    transcoder = RichTriggerConditionTranscoderFactory.make_rich_trigger_condition_transcoder(
                        condition_id
                    )
                    conditions.append(
                        transcoder.decode(condition, rich_chk_decode_context)
                    )
                else:
                    conditions.append(condition)
        return conditions

    def _decode_actions(
        self,
        decoded_actions: list[DecodedTriggerAction],
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> list[Union[RichTriggerAction, DecodedTriggerAction]]:
        actions: list[Union[RichTriggerAction, DecodedTriggerAction]] = []
        for action in decoded_actions:
            if not TriggerActionId.contains(action.action_id):
                self.log.error(
                    f"Unknown trigger action ID: {action.action_id}!  "
                    f"Make sure all action bytes are accounted for in the enum."
                )
                actions.append(action)
            else:
                action_id = TriggerActionId.get_by_id(action.action_id)
                if RichTriggerActionTranscoderFactory.supports_transcoding_trig_action(
                    action_id
                ):
                    transcoder = RichTriggerActionTranscoderFactory.make_rich_trigger_action_transcoder(
                        action_id
                    )
                    actions.append(transcoder.decode(action, rich_chk_decode_context))
                else:
                    actions.append(action)
        return actions

    def _decode_player_execution(
        self, player_execution: DecodedPlayerExecution
    ) -> set[PlayerId]:
        players = set()
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
            if not PlayerId.contains(maybe_player_id):
                msg = f"Missing player ID value in PlayerId enum, got unexpected value: {maybe_player_id}."
                self.log.error(msg)
                raise ValueError(msg)
            player_id = PlayerId.get_by_id(maybe_player_id)
            if is_used:
                players.add(player_id)
        return players

    def encode(
        self,
        rich_chk_section: RichTrigSection,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedTrigSection:
        decoded_triggers = [
            self._encode_trigger(trigger, rich_chk_encode_context)
            for trigger in rich_chk_section.triggers
        ]
        return DecodedTrigSection(_triggers=decoded_triggers)

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
        conditions: list[Union[RichTriggerCondition, DecodedTriggerCondition]],
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> list[DecodedTriggerCondition]:
        decoded_conditions = []
        for condition in conditions:
            if isinstance(condition, DecodedTriggerCondition):
                decoded_conditions.append(condition)
            else:
                if RichTriggerConditionTranscoderFactory.supports_transcoding_trig_action(
                    condition.condition_id()
                ):
                    transcoder = RichTriggerConditionTranscoderFactory.make_rich_trigger_condition_transcoder(
                        condition.condition_id()
                    )
                    conditions.append(
                        transcoder.encode(condition, rich_chk_encode_context)
                    )
                else:
                    msg = (
                        f"Unhandled RichTriggerCondition that can't be "
                        f"decoded back due to missing transcoder: {condition}"
                    )
                    self.log.error(msg)
                    raise ValueError(msg)
        return decoded_conditions

    def _encode_actions(
        self,
        actions: list[Union[RichTriggerAction, DecodedTriggerAction]],
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> list[DecodedTriggerAction]:
        decoded_actions = []
        for action in actions:
            if isinstance(action, DecodedTriggerAction):
                decoded_actions.append(action)
            else:
                if RichTriggerActionTranscoderFactory.supports_transcoding_trig_action(
                    action.action_id()
                ):
                    transcoder = RichTriggerActionTranscoderFactory.make_rich_trigger_action_transcoder(
                        action.action_id()
                    )
                    decoded_actions.append(
                        transcoder.encode(action, rich_chk_encode_context)
                    )
                else:
                    msg = (
                        f"Unhandled RichTriggerAction that can't be "
                        f"decoded back due to missing transcoder: {action}"
                    )
                    self.log.error(msg)
                    raise ValueError(msg)
        return decoded_actions

    def _encode_player_execution(
        self, players: set[PlayerId]
    ) -> DecodedPlayerExecution:
        player_flags = []
        for player_id in PlayerId:
            if player_id in players:
                player_flags.append(1)
            else:
                player_flags.append(0)
        return DecodedPlayerExecution(
            _execution_flags=0, _player_flags=player_flags, _current_action_index=0
        )
