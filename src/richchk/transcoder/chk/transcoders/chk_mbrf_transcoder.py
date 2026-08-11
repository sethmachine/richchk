"""Decode and encode the MBRF section which contains all mission briefings.

The MBRF section uses exactly the same binary format as the TRIG section: each entry is
2400 bytes with 16 conditions (20 bytes each), 64 actions (32 bytes each), and a 32-byte
player execution block. The only distinction is that all 16 condition slots are null
except the first, which has condition byte 13 to mark it as a mission briefing.
"""
import struct
from io import BytesIO

from ....model.chk.mbrf.decoded_mbrf_section import DecodedMbrfSection
from ....model.chk.trig.decoded_player_execution import DecodedPlayerExecution
from ....model.chk.trig.decoded_trigger import DecodedTrigger
from ....model.chk.trig.decoded_trigger_action import DecodedTriggerAction
from ....model.chk.trig.decoded_trigger_condition import DecodedTriggerCondition
from ....transcoder.chk.chk_section_transcoder import ChkSectionTranscoder
from ....transcoder.chk.chk_section_transcoder_factory import _RegistrableTranscoder


class ChkMbrfTranscoder(
    ChkSectionTranscoder[DecodedMbrfSection],
    _RegistrableTranscoder,
    chk_section_name=DecodedMbrfSection.section_name(),
):
    _NUM_CONDITIONS_PER_TRIGGER = 16
    _NUM_ACTIONS_PER_TRIGGER = 64
    _NUM_PLAYER_EXECUTION_IDS = 27

    _NUM_BYTES_PER_CONDITION = 20
    _NUM_BYTES_PER_ACTION = 32
    _NUM_BYTES_PER_PLAYER_EXECUTION = 32
    _NUM_BYTES_PER_TRIGGER = (
        _NUM_BYTES_PER_CONDITION * _NUM_CONDITIONS_PER_TRIGGER
        + _NUM_BYTES_PER_ACTION * _NUM_ACTIONS_PER_TRIGGER
        + _NUM_BYTES_PER_PLAYER_EXECUTION
    )

    _NUM_VALUES_PER_CONDITION = 9
    _NUM_VALUES_PER_ACTION = 12

    _CONDITION_FORMAT = "3I H 4B H"
    _ACTION_FORMAT = "6I H 3B B H"
    _PLAYER_EXECUTION_FORMAT = "I 27B B"

    _ALL_CONDITIONS_FORMAT = _CONDITION_FORMAT * _NUM_CONDITIONS_PER_TRIGGER
    _ALL_ACTIONS_FORMAT = _ACTION_FORMAT * _NUM_ACTIONS_PER_TRIGGER

    def decode(self, chk_section_binary_data: bytes) -> DecodedMbrfSection:
        num_triggers = len(chk_section_binary_data) // self._NUM_BYTES_PER_TRIGGER
        triggers = []
        bytes_stream: BytesIO = BytesIO(chk_section_binary_data)
        for _ in range(num_triggers):
            triggers.append(
                self._decode_single_trigger(
                    bytes_stream.read(self._NUM_BYTES_PER_TRIGGER)
                )
            )
        return DecodedMbrfSection(_triggers=triggers)

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
        values = struct.unpack(
            cls._ALL_CONDITIONS_FORMAT,
            bytes_stream.read(
                cls._NUM_BYTES_PER_CONDITION * cls._NUM_CONDITIONS_PER_TRIGGER
            ),
        )
        conditions = []
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
            _player_flags=list(values[1:28]),
            _current_action_index=values[28],
        )

    def _encode(self, decoded_chk_section: DecodedMbrfSection) -> bytes:
        total_size = len(decoded_chk_section.triggers) * self._NUM_BYTES_PER_TRIGGER
        data = bytearray(total_size)
        offset = 0
        for trigger in decoded_chk_section.triggers:
            self._encode_trigger_into(trigger, data, offset)
            offset += self._NUM_BYTES_PER_TRIGGER
        return bytes(data)

    @classmethod
    def _encode_trigger_into(
        cls, trigger: DecodedTrigger, data: bytearray, base_offset: int
    ) -> None:
        cond_offset = base_offset
        for condition in trigger._conditions:
            cid = condition._condition_id
            if not cid:
                break
            struct.pack_into(
                cls._CONDITION_FORMAT,
                data,
                cond_offset,
                condition._location_id,
                condition._group,
                condition._quantity,
                condition._unit_id,
                condition._numeric_comparison_operation,
                cid,
                condition._numeric_comparand_type,
                condition._flags,
                condition._mask_flag,
            )
            cond_offset += cls._NUM_BYTES_PER_CONDITION

        act_base = (
            base_offset + cls._NUM_BYTES_PER_CONDITION * cls._NUM_CONDITIONS_PER_TRIGGER
        )
        act_offset = act_base
        for action in trigger._actions:
            aid = action._action_id
            if not aid:
                break
            struct.pack_into(
                cls._ACTION_FORMAT,
                data,
                act_offset,
                action._location_id,
                action._text_string_id,
                action._wav_string_id,
                action._time,
                action._first_group,
                action._second_group,
                action._action_argument_type,
                aid,
                action._quantifier_or_switch_or_order,
                action._flags,
                action._padding,
                action._mask_flag,
            )
            act_offset += cls._NUM_BYTES_PER_ACTION

        pe_base = act_base + cls._NUM_BYTES_PER_ACTION * cls._NUM_ACTIONS_PER_TRIGGER
        pe = trigger._player_execution
        buf = bytearray(cls._NUM_BYTES_PER_PLAYER_EXECUTION)
        struct.pack_into(
            cls._PLAYER_EXECUTION_FORMAT,
            buf,
            0,
            pe._execution_flags,
            *pe._player_flags,
            pe._current_action_index,
        )
        data[pe_base : pe_base + cls._NUM_BYTES_PER_PLAYER_EXECUTION] = buf
