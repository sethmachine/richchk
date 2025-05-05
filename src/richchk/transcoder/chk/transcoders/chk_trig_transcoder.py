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
    # Counts of elements
    _NUM_CONDITIONS_PER_TRIGGER = 16
    _NUM_ACTIONS_PER_TRIGGER = 64
    _NUM_PLAYER_EXECUTION_IDS = 27

    # Byte sizes for each component
    _NUM_BYTES_PER_CONDITION = 20  # 3*4 + 2 + 4*1 + 2
    _NUM_BYTES_PER_ACTION = 32  # 6*4 + 2 + 3*1 + 1 + 2
    _NUM_BYTES_PER_PLAYER_EXECUTION = 32  # 4 + 27*1 + 1
    _NUM_BYTES_PER_TRIGGER = (
        _NUM_BYTES_PER_CONDITION * _NUM_CONDITIONS_PER_TRIGGER
        + _NUM_BYTES_PER_ACTION * _NUM_ACTIONS_PER_TRIGGER
        + _NUM_BYTES_PER_PLAYER_EXECUTION
    )

    # Values per struct
    # location_id, group, quantity, unit_id, numeric_comparison_operation, condition_id,
    # numeric_comparand_type, flags, mask_flag
    _NUM_VALUES_PER_CONDITION = 9

    # location_id, text_string_id, wav_string_id, time, first_group, second_group,
    # action_argument_type, action_id, quantifier_or_switch_or_order, flags, padding, mask_flag
    _NUM_VALUES_PER_ACTION = 12

    # Format strings for struct packing
    _CONDITION_FORMAT = "3I H 4B H"  # 20 bytes: 3*4 + 2 + 4*1 + 2
    _ACTION_FORMAT = "6I H 3B B H"  # 32 bytes: 6*4 + 2 + 3*1 + 1 + 2
    _PLAYER_EXECUTION_FORMAT = "I 27B B"  # 32 bytes: 4 + 27*1 + 1

    # Bulk format strings for decoding multiple items at once
    _ALL_CONDITIONS_FORMAT = (
        _CONDITION_FORMAT * _NUM_CONDITIONS_PER_TRIGGER
    )  # 16 conditions
    _ALL_ACTIONS_FORMAT = _ACTION_FORMAT * _NUM_ACTIONS_PER_TRIGGER  # 64 actions

    def decode(self, chk_section_binary_data: bytes) -> DecodedTrigSection:
        num_triggers = len(chk_section_binary_data) // self._NUM_BYTES_PER_TRIGGER
        triggers = []

        bytes_stream: BytesIO = BytesIO(chk_section_binary_data)
        for i in range(num_triggers):
            triggers.append(
                self._decode_single_trigger(
                    bytes_stream.read(self._NUM_BYTES_PER_TRIGGER)
                )
            )
        return DecodedTrigSection(_triggers=triggers)

    @classmethod
    def _decode_single_trigger(cls, trigger_bytes: bytes) -> DecodedTrigger:
        bytes_stream: BytesIO = BytesIO(trigger_bytes)
        conditions = cls._decode_conditions_for_single_trigger(bytes_stream)
        actions = cls._decode_actions_for_single_trigger(bytes_stream)
        player_execution = cls._decode_player_execution_for_single_trigger(bytes_stream)

        return DecodedTrigger(
            _conditions=conditions, _actions=actions, _player_execution=player_execution
        )

    @classmethod
    def _decode_conditions_for_single_trigger(
        cls, bytes_stream: BytesIO
    ) -> list[DecodedTriggerCondition]:
        # Read all conditions at once
        values = struct.unpack(
            cls._ALL_CONDITIONS_FORMAT,
            bytes_stream.read(
                cls._NUM_BYTES_PER_CONDITION * cls._NUM_CONDITIONS_PER_TRIGGER
            ),
        )

        conditions = []  # Pre-allocate list
        for i in range(cls._NUM_CONDITIONS_PER_TRIGGER):
            base = i * cls._NUM_VALUES_PER_CONDITION
            conditions.append(
                DecodedTriggerCondition(
                    _location_id=values[base],
                    _group=values[base + 1],
                    _quantity=values[base + 2],
                    _unit_id=values[base + 3],
                    _numeric_comparison_operation=values[base + 4],
                    _condition_id=values[base + 5],
                    _numeric_comparand_type=values[base + 6],
                    _flags=values[base + 7],
                    _mask_flag=values[base + 8],
                )
            )
        return conditions

    @classmethod
    def _decode_actions_for_single_trigger(
        cls, bytes_stream: BytesIO
    ) -> list[DecodedTriggerAction]:
        # Read all actions at once
        values = struct.unpack(
            cls._ALL_ACTIONS_FORMAT,
            bytes_stream.read(cls._NUM_BYTES_PER_ACTION * cls._NUM_ACTIONS_PER_TRIGGER),
        )

        actions = []
        for i in range(cls._NUM_ACTIONS_PER_TRIGGER):
            base = i * cls._NUM_VALUES_PER_ACTION
            actions.append(
                DecodedTriggerAction(
                    _location_id=values[base],
                    _text_string_id=values[base + 1],
                    _wav_string_id=values[base + 2],
                    _time=values[base + 3],
                    _first_group=values[base + 4],
                    _second_group=values[base + 5],
                    _action_argument_type=values[base + 6],
                    _action_id=values[base + 7],
                    _quantifier_or_switch_or_order=values[base + 8],
                    _flags=values[base + 9],
                    _padding=values[base + 10],
                    _mask_flag=values[base + 11],
                )
            )
        return actions

    @classmethod
    def _decode_player_execution_for_single_trigger(
        cls, bytes_stream: BytesIO
    ) -> DecodedPlayerExecution:
        values = struct.unpack(
            cls._PLAYER_EXECUTION_FORMAT,
            bytes_stream.read(cls._NUM_BYTES_PER_PLAYER_EXECUTION),
        )
        return DecodedPlayerExecution(
            _execution_flags=values[0],
            _player_flags=list(values[1:28]),  # 27 player flags
            _current_action_index=values[28],
        )

    def _encode(self, decoded_chk_section: DecodedTrigSection) -> bytes:
        # Pre-calculate total size needed
        total_size = len(decoded_chk_section.triggers) * self._NUM_BYTES_PER_TRIGGER
        data = bytearray(total_size)
        offset = 0

        for trigger in decoded_chk_section.triggers:
            # Encode directly into the main bytearray
            self._encode_trigger_into(trigger, data, offset)
            offset += self._NUM_BYTES_PER_TRIGGER

        return bytes(data)

    @classmethod
    def _encode_trigger_into(
        cls, trigger: DecodedTrigger, data: bytearray, base_offset: int
    ) -> None:
        offset = base_offset

        # Pack all conditions at once
        all_condition_values = []
        for condition in trigger.conditions:
            all_condition_values.extend(
                [
                    condition.location_id,
                    condition.group,
                    condition.quantity,
                    condition.unit_id,
                    condition.numeric_comparison_operation,
                    condition.condition_id,
                    condition.numeric_comparand_type,
                    condition.flags,
                    condition.mask_flag,
                ]
            )
        struct.pack_into(
            cls._ALL_CONDITIONS_FORMAT, data, offset, *all_condition_values
        )
        offset += cls._NUM_BYTES_PER_CONDITION * cls._NUM_CONDITIONS_PER_TRIGGER

        # Pack all actions at once
        all_action_values = []
        for action in trigger.actions:
            all_action_values.extend(
                [
                    action.location_id,
                    action.text_string_id,
                    action.wav_string_id,
                    action.time,
                    action.first_group,
                    action.second_group,
                    action.action_argument_type,
                    action.action_id,
                    action.quantifier_or_switch_or_order,
                    action.flags,
                    action.padding,
                    action.mask_flag,
                ]
            )
        struct.pack_into(cls._ALL_ACTIONS_FORMAT, data, offset, *all_action_values)
        offset += cls._NUM_BYTES_PER_ACTION * cls._NUM_ACTIONS_PER_TRIGGER

        # Pack player execution
        struct.pack_into(
            cls._PLAYER_EXECUTION_FORMAT,
            data,
            offset,
            trigger.player_execution.execution_flags,
            *trigger.player_execution.player_flags,
            trigger.player_execution.current_action_index,
        )
