"""Decode and encode the TRIG section which contains all map triggers.

Required for all versions. Not required for Melee. Validation: Must be a multiple of
2400 bytes.

This section contains all the triggers in the map. This along with MBRF is the most
complicated section in the entire scenario.chk file as there is a lot of data packed
into too little of a space. Refer to the appendix at the bottom of this page for more
information. For easy reference, since each trigger contains 2400 bytes, the amount of
triggers can be gotten by taking the section length and dividing by 2400. Every single
trigger in the map will have the following format:

16 Conditions (20 byte struct) Every trigger has 16 of the following format, even if
only one condition is used. See the appendix for information on which items are used for
what conditions.

u32: Location number for the condition (1 based -- 0 refers to No Location), EUD Bitmask
for a Death condition if the MaskFlag is set to "SC"

u32: Group that the condition applies to

u32: Qualified number (how many/resource amount)

u16: Unit ID condition applies to

u8: Numeric comparison, switch state

u8: Condition byte

u8: Resource type, score type, Switch number (0-based)

u8: Flags

Bit 0 - Unknown/unused

Bit 1 - Enabled flag. If on, the trigger action/condition is disabled/ignored

Bit 2 - Always display flag.

Bit 3 - Unit properties is used. (Note: This is used in *.trg files)

 Bit 4 - Unit type is used. Cleared in "Offset + Mask" EUD conditions. May not be
necessary otherwise?

Bit 5-7 - Unknown/unused

u16: MaskFlag: set to "SC" (0x53, 0x43) when using the bitmask for EUDs, 0 otherwise

64 Actions (32 byte struct) Immediately following the 16 conditions, there are 64
actions. There will always be 64 of the following structure, even if some of them are
unused.

 u32: Location - source location in "Order" and "Move Unit", dest location in "Move
Location" (1 based -- 0 refers to No Location), EUD Bitmask for a Death action if the
MaskFlag is set to "SC"

u32: String number for trigger text (0 means no string)

u32: WAV string number (0 means no string)

u32: Seconds/milliseconds of time

u32: First (or only) Group/Player affected.

 u32: Second group affected, secondary location (1-based), CUWP #, number, AI script
(4-byte string), switch (0-based #)

u16: Unit type, score type, resource type, alliance status

u8: Action byte

u8: Number of units (0 means All Units), action state, unit order, number modifier

u8: Flags

Bit 0 - Ignore a wait/transmission once.

Bit 1 - Enabled flag. If on, the trigger action/condition is disabled.

 Bit 2 - Always display flag - when not set: if the user has turned off subtitles (see
sound options) the text will not display, when set: text will always display

Bit 3 - Unit properties is used. Staredit uses this for *.trg files.

Bit 4 - Unit type is used. Cleared in "Offset + Mask" EUD actions.

Bit 5-7 - Unknown/unused

u8: Padding

 u16 (2 bytes): MaskFlag: set to "SC" (0x53, 0x43) when using the bitmask for EUDs, 0
otherwise

Player Execution

Following the 16 conditions and 64 actions, every trigger also has this structure

u32: execution flags

Bit 0 - All conditions are met, executing actions, cleared on the next trigger loop.

Bit 1 - Ignore the following actions: Defeat, Draw.

Bit 2 - Preserve trigger. (Can replace Preserve Trigger action)

Bit 3 - Ignore execution.

 Bit 4 - Ignore all of the following actions for this trigger until the next trigger
loop: Wait, PauseGame, Transmission, PlayWAV, DisplayTextMessage, CenterView,
MinimapPing, TalkingPortrait, and MuteUnitSpeech.

 Bit 5 - This trigger has paused the game, ignoring subsequent calls to Pause Game
(Unpause Game clears this flag only in the same trigger), may automatically call unpause
at the end of action execution?

Bit 6 - Wait skipping disabled for this trigger, cleared on next trigger loop.

Bit 7-31 - Unknown/unused

u8[27]: 1 byte for each player in the #List of Players/Group IDs

00 - Trigger is not executed for player

01 - Trigger is executed for player

u8: Index of the current action, in StarCraft this is incremented after each action is
executed, trigger execution ends when this is 64 (Max Actions) or an action is
encountered with Action byte as 0 This section can be split. Additional TRIG sections
will add more triggers.
"""
import struct
from io import BytesIO

from ....model.chk.trig.decoded_player_execution import DecodedPlayerExecution
from ....model.chk.trig.decoded_trig_section import DecodedTrigSection
from ....model.chk.trig.decoded_trigger import DecodedTrigger
from ....model.chk.trig.decoded_trigger_action import DecodedTriggerAction
from ....model.chk.trig.decoded_trigger_condition import DecodedTriggerCondition
from ....transcoder.chk.chk_section_transcoder import ChkSectionTranscoder
from ....transcoder.chk.chk_section_transcoder_factory import _RegistrableTranscoder


class ChkTrigTranscoder(
    ChkSectionTranscoder[DecodedTrigSection],
    _RegistrableTranscoder,
    chk_section_name=DecodedTrigSection.section_name(),
):
    _NUM_BYTES_PER_TRIGGER = 2400
    _NUM_CONDITIONS_PER_TRIGGER = 16
    _NUM_ACTIONS_PER_TRIGGER = 64
    _NUM_PLAYER_EXECUTION_IDS = 27

    def decode(self, chk_section_binary_data: bytes) -> DecodedTrigSection:
        bytes_stream: BytesIO = BytesIO(chk_section_binary_data)
        triggers: list[DecodedTrigger] = []
        while bytes_stream.tell() != len(chk_section_binary_data):
            triggers.append(
                self._decode_single_trigger(
                    bytes_stream.read(self._NUM_BYTES_PER_TRIGGER)
                )
            )
        return DecodedTrigSection(_triggers=triggers)

    @classmethod
    def _decode_single_trigger(cls, trigger_bytes: bytes) -> DecodedTrigger:
        bytes_stream: BytesIO = BytesIO(trigger_bytes)
        conditions: list[
            DecodedTriggerCondition
        ] = cls._decode_conditions_for_single_trigger(bytes_stream)
        actions: list[DecodedTriggerAction] = cls._decode_actions_for_single_trigger(
            bytes_stream
        )
        player_execution = cls._decode_player_execution_for_single_trigger(bytes_stream)

        return DecodedTrigger(
            _conditions=conditions, _actions=actions, _player_execution=player_execution
        )

    @classmethod
    def _decode_conditions_for_single_trigger(
        cls, bytes_stream: BytesIO
    ) -> list[DecodedTriggerCondition]:
        conditions: list[DecodedTriggerCondition] = []
        # there are always 16 conditions, even if not all are used
        for _ in range(cls._NUM_CONDITIONS_PER_TRIGGER):
            location_id = struct.unpack("I", bytes_stream.read(4))[0]
            group = struct.unpack("I", bytes_stream.read(4))[0]
            quantity = struct.unpack("I", bytes_stream.read(4))[0]
            unit_id = struct.unpack("H", bytes_stream.read(2))[0]
            numeric_comparison_operation = struct.unpack("B", bytes_stream.read(1))[0]
            condition_id = struct.unpack("B", bytes_stream.read(1))[0]
            numeric_comparand_type = struct.unpack("B", bytes_stream.read(1))[0]
            flags = struct.unpack("B", bytes_stream.read(1))[0]
            mask_flag = struct.unpack("H", bytes_stream.read(2))[0]
            conditions.append(
                DecodedTriggerCondition(
                    _location_id=location_id,
                    _group=group,
                    _quantity=quantity,
                    _unit_id=unit_id,
                    _numeric_comparison_operation=numeric_comparison_operation,
                    _condition_id=condition_id,
                    _numeric_comparand_type=numeric_comparand_type,
                    _flags=flags,
                    _mask_flag=mask_flag,
                )
            )
        return conditions

    @classmethod
    def _decode_actions_for_single_trigger(
        cls, bytes_stream: BytesIO
    ) -> list[DecodedTriggerAction]:
        actions: list[DecodedTriggerAction] = []
        # there are always 64 conditions, even if not all are used
        for _ in range(cls._NUM_ACTIONS_PER_TRIGGER):
            location_id = struct.unpack("I", bytes_stream.read(4))[0]
            text_string_id = struct.unpack("I", bytes_stream.read(4))[0]
            wav_string_id = struct.unpack("I", bytes_stream.read(4))[0]
            time_ = struct.unpack("I", bytes_stream.read(4))[0]
            first_group = struct.unpack("I", bytes_stream.read(4))[0]
            second_group = struct.unpack("I", bytes_stream.read(4))[0]
            action_argument_type = struct.unpack("H", bytes_stream.read(2))[0]
            action_id = struct.unpack("B", bytes_stream.read(1))[0]
            quantifier_or_switch_or_order = struct.unpack("B", bytes_stream.read(1))[0]
            flags = struct.unpack("B", bytes_stream.read(1))[0]
            padding = struct.unpack("B", bytes_stream.read(1))[0]
            mask_flag = struct.unpack("H", bytes_stream.read(2))[0]
            actions.append(
                DecodedTriggerAction(
                    _location_id=location_id,
                    _text_string_id=text_string_id,
                    _wav_string_id=wav_string_id,
                    _time=time_,
                    _first_group=first_group,
                    _second_group=second_group,
                    _action_argument_type=action_argument_type,
                    _action_id=action_id,
                    _quantifier_or_switch_or_order=quantifier_or_switch_or_order,
                    _flags=flags,
                    _padding=padding,
                    _mask_flag=mask_flag,
                )
            )
        return actions

    @classmethod
    def _decode_player_execution_for_single_trigger(
        cls, bytes_stream: BytesIO
    ) -> DecodedPlayerExecution:
        execution_flags = struct.unpack("I", bytes_stream.read(4))[0]
        player_flags = [
            struct.unpack("B", bytes_stream.read(1))[0]
            for _ in range(cls._NUM_PLAYER_EXECUTION_IDS)
        ]
        _current_action_index = struct.unpack("B", bytes_stream.read(1))[0]
        return DecodedPlayerExecution(
            _execution_flags=execution_flags,
            _player_flags=player_flags,
            _current_action_index=_current_action_index,
        )

    def _encode(self, decoded_chk_section: DecodedTrigSection) -> bytes:
        # Pre-calculate total size needed
        total_size = len(decoded_chk_section.triggers) * self._NUM_BYTES_PER_TRIGGER
        data = bytearray(total_size)
        offset = 0

        for trigger in decoded_chk_section.triggers:
            # Encode each trigger's data into the pre-allocated bytearray
            trigger_data = self._encode_trigger(trigger)
            data[offset : offset + self._NUM_BYTES_PER_TRIGGER] = trigger_data
            offset += self._NUM_BYTES_PER_TRIGGER

        return bytes(data)

    @classmethod
    def _encode_trigger(cls, trigger: DecodedTrigger) -> bytes:
        # Pre-calculate size for a single trigger
        data = bytearray(cls._NUM_BYTES_PER_TRIGGER)
        offset = 0

        # Encode conditions
        for condition in trigger.conditions:
            condition_data = cls._encode_condition(condition)
            data[offset : offset + len(condition_data)] = condition_data
            offset += len(condition_data)

        # Encode actions
        for action in trigger.actions:
            action_data = cls._encode_action(action)
            data[offset : offset + len(action_data)] = action_data
            offset += len(action_data)

        # Encode player execution
        player_execution_data = cls._encode_player_execution(trigger.player_execution)
        data[offset : offset + len(player_execution_data)] = player_execution_data

        return bytes(data)

    @classmethod
    def _encode_condition(cls, condition: DecodedTriggerCondition) -> bytes:
        data = bytearray()
        data.extend(struct.pack("I", condition.location_id))
        data.extend(struct.pack("I", condition.group))
        data.extend(struct.pack("I", condition.quantity))
        data.extend(struct.pack("H", condition.unit_id))
        data.extend(struct.pack("B", condition.numeric_comparison_operation))
        data.extend(struct.pack("B", condition.condition_id))
        data.extend(struct.pack("B", condition.numeric_comparand_type))
        data.extend(struct.pack("B", condition.flags))
        data.extend(struct.pack("H", condition.mask_flag))
        return bytes(data)

    @classmethod
    def _encode_action(cls, action: DecodedTriggerAction) -> bytes:
        data = bytearray()
        data.extend(struct.pack("I", action.location_id))
        data.extend(struct.pack("I", action.text_string_id))
        data.extend(struct.pack("I", action.wav_string_id))
        data.extend(struct.pack("I", action.time))
        data.extend(struct.pack("I", action.first_group))
        data.extend(struct.pack("I", action.second_group))
        data.extend(struct.pack("H", action.action_argument_type))
        data.extend(struct.pack("B", action.action_id))
        data.extend(struct.pack("B", action.quantifier_or_switch_or_order))
        data.extend(struct.pack("B", action.flags))
        data.extend(struct.pack("B", action.padding))
        data.extend(struct.pack("H", action.mask_flag))
        return bytes(data)

    @classmethod
    def _encode_player_execution(
        cls, player_execution: DecodedPlayerExecution
    ) -> bytes:
        data = bytearray()
        data.extend(struct.pack("I", player_execution.execution_flags))
        data.extend(
            struct.pack(
                "{}B".format(len(player_execution.player_flags)),
                *player_execution.player_flags
            )
        )
        data.extend(struct.pack("B", player_execution.current_action_index))
        return bytes(data)
