"""Decode the TRIG - Triggers section."""
import array
import struct
import sys
from typing import Any, ClassVar, Optional, Union, cast

from ....model.chk.trig.decoded_player_execution import DecodedPlayerExecution
from ....model.chk.trig.decoded_trig_section import DecodedTrigSection
from ....model.chk.trig.decoded_trigger import DecodedTrigger
from ....model.chk.trig.decoded_trigger_action import DecodedTriggerAction
from ....model.chk.trig.decoded_trigger_condition import DecodedTriggerCondition
from ....model.richchk.richchk_decode_context import RichChkDecodeContext
from ....model.richchk.richchk_encode_context import RichChkEncodeContext
from ....model.richchk.trig.actions.flags.trigger_action_flags import (
    _DEFAULT_TRIGGER_ACTION_FLAGS,
)
from ....model.richchk.trig.actions.preserve_trigger_action import PreserveTrigger
from ....model.richchk.trig.actions.set_deaths_action import SetDeathsAction
from ....model.richchk.trig.conditions.deaths_condition import DeathsCondition
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
from .trig.rich_trigger_action_transcoder_factory import (
    RichTriggerActionTranscoderFactory,
)
from .trig.rich_trigger_condition_transcoder_factory import (
    RichTriggerConditionTranscoderFactory,
)

_IS_BIG_ENDIAN: bool = sys.byteorder == "big"


class RichChkTrigTranscoder(
    RichChkSectionTranscoder[RichTrigSection, DecodedTrigSection],
    _RichChkRegistrableTranscoder,
    chk_section_name=DecodedTrigSection.section_name(),
):

    _NUM_CONDITIONS_PER_TRIGGER = 16
    _NUM_ACTIONS_PER_TRIGGER = 64

    # Binary format constants (mirrored from ChkTrigTranscoder)
    _CONDITION_FORMAT = "3I H 4B H"
    _ACTION_FORMAT = "6I H 3B B H"
    _PLAYER_EXECUTION_FORMAT = "I 27B B"
    _NUM_BYTES_PER_CONDITION = 20
    _NUM_BYTES_PER_ACTION = 32
    _NUM_BYTES_PER_PE = 32
    _CONDS_SECTION_SIZE = _NUM_BYTES_PER_CONDITION * _NUM_CONDITIONS_PER_TRIGGER  # 320
    _ACTS_SECTION_SIZE = _NUM_BYTES_PER_ACTION * _NUM_ACTIONS_PER_TRIGGER  # 2048
    _NUM_BYTES_PER_TRIGGER = (
        _CONDS_SECTION_SIZE + _ACTS_SECTION_SIZE + _NUM_BYTES_PER_PE
    )

    # Inline IDs for the most common condition/action types
    _DEATHS_CID: int = DeathsCondition.condition_id().id
    _SET_DEATHS_AID: int = SetDeathsAction.action_id().id
    _PRESERVE_AID: int = PreserveTrigger.action_id().id

    # Pre-packed 32 bytes for a PreserveTrigger action (all zeros except action_id byte)
    _PRESERVE_TRIGGER_BYTES: ClassVar[bytes] = struct.pack(
        "6I H 3B B H", 0, 0, 0, 0, 0, 0, 0, PreserveTrigger.action_id().id, 0, 0, 0, 0
    )
    _COND_STRUCT: ClassVar[struct.Struct] = struct.Struct(_CONDITION_FORMAT)
    _ACT_STRUCT: ClassVar[struct.Struct] = struct.Struct(_ACTION_FORMAT)
    _PE_STRUCT: ClassVar[struct.Struct] = struct.Struct(_PLAYER_EXECUTION_FORMAT)

    _action_type_cache: ClassVar[dict[Any, Any]] = {}
    _condition_type_cache: ClassVar[dict[Any, Any]] = {}
    _fused_pe_bytes_cache: ClassVar[dict[Any, Any]] = {}
    _I_STRUCT: ClassVar[struct.Struct] = struct.Struct("<I")
    _template_cache: ClassVar[
        dict[Any, Any]
    ] = (
        {}
    )  # id(triggers) → (nz_pairs, template_bytes, cond_patches, act_patches) or False
    _template_fingerprint_cache: ClassVar[
        dict[Any, Any]
    ] = (
        {}
    )  # structural fingerprint → (nz_pairs, template_bytes, cond_patches, act_patches)
    _nz_bufs_cache: ClassVar[
        dict[Any, Any]
    ] = {}  # (id(nz_pairs), n) → [(pos, buf)] pre-built strided write buffers

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
        raw_bytes = self._fused_encode_to_bytes(
            rich_chk_section, rich_chk_encode_context
        )
        return DecodedTrigSection(_triggers=[], _raw_data=raw_bytes)

    @staticmethod
    def _compute_trigger_fingerprint(
        conds0: Any, acts0: Any, players0: Any
    ) -> tuple[Any, ...]:
        return (
            tuple((c._group, c._unit, c._comparator) for c in conds0),
            tuple(
                (a._group, a._unit, a._amount_modifier)
                if type(a) is SetDeathsAction
                else ()
                for a in acts0
            ),
            players0,
        )

    def _build_template_info(self, triggers: Any) -> Any:
        """Try to build a per-trigger template for uniform
        DeathsCondition+SetDeaths+Preserve batches.

        Returns (template_bytes, cond_patches, act_patches) if all triggers share the
        same non-amount fields, else False. cond_patches: tuple of (cond_index,
        byte_offset_within_trigger) for varying amounts act_patches: tuple of
        (act_index, byte_offset_within_trigger) for varying amounts
        """
        if not triggers:
            return False
        t0 = triggers[0]
        conds0 = t0._conditions
        acts0 = t0._actions
        players0 = t0._players
        n_conds = len(conds0)
        n_acts = len(acts0)

        for c in conds0:
            if (
                type(c) is not DeathsCondition
                or c._flags is not _DEFAULT_TRIGGER_CONDITION_FLAGS
            ):
                return False
        for a in acts0:
            at = type(a)
            if at is SetDeathsAction:
                if a._flags is not _DEFAULT_TRIGGER_ACTION_FLAGS:
                    return False
            elif at is not PreserveTrigger:
                return False

        fingerprint = self._compute_trigger_fingerprint(conds0, acts0, players0)
        fp_result = self._template_fingerprint_cache.get(fingerprint)
        if fp_result is not None:
            return fp_result

        cond_amounts_vary = [False] * n_conds
        act_amounts_vary = [False] * n_acts
        check_count = min(len(triggers), 200)
        for i_check in range(check_count):
            t = triggers[i_check]
            if len(t._conditions) != n_conds or len(t._actions) != n_acts:
                return False
            if t._players != players0:
                return False
            for i in range(n_conds):
                c = t._conditions[i]
                c0 = conds0[i]
                if (
                    type(c) is not DeathsCondition
                    or c._flags is not _DEFAULT_TRIGGER_CONDITION_FLAGS
                    or c._group is not c0._group
                    or c._unit is not c0._unit
                    or c._comparator is not c0._comparator
                ):
                    return False
                if c._amount != c0._amount:
                    cond_amounts_vary[i] = True
            for j in range(n_acts):
                a = t._actions[j]
                a0 = acts0[j]
                at = type(a)
                if at is not type(a0):
                    return False
                if at is SetDeathsAction:
                    if (
                        a._flags is not _DEFAULT_TRIGGER_ACTION_FLAGS
                        or a._group is not a0._group
                        or a._unit is not a0._unit
                        or a._amount_modifier is not a0._amount_modifier
                    ):
                        return False
                    if a._amount != a0._amount:
                        act_amounts_vary[j] = True
                elif at is not PreserveTrigger:
                    return False

        trig_sz = self._NUM_BYTES_PER_TRIGGER
        template = bytearray(trig_sz)
        pack_into_cond = self._COND_STRUCT.pack_into
        pack_into_act = self._ACT_STRUCT.pack_into
        pack_into_pe = self._PE_STRUCT.pack_into
        conds_sz = self._CONDS_SECTION_SIZE
        deaths_cid = self._DEATHS_CID
        set_deaths_aid = self._SET_DEATHS_AID

        cond_patches = []
        cond_off = 0
        for i, c in enumerate(conds0):
            tmpl_amount = 0 if cond_amounts_vary[i] else c._amount
            pack_into_cond(
                template,
                cond_off,
                0,
                c._group._id,
                tmpl_amount,
                c._unit._id,
                c._comparator._id,
                deaths_cid,
                0,
                0,
                0,
            )
            if cond_amounts_vary[i]:
                cond_patches.append((i, cond_off + 8))
            cond_off += self._NUM_BYTES_PER_CONDITION

        act_patches = []
        act_off = conds_sz
        for j, a in enumerate(acts0):
            at = type(a)
            if at is SetDeathsAction:
                tmpl_amount = 0 if act_amounts_vary[j] else a._amount
                pack_into_act(
                    template,
                    act_off,
                    0,
                    0,
                    0,
                    0,
                    a._group._id,
                    tmpl_amount,
                    a._unit._id,
                    set_deaths_aid,
                    a._amount_modifier._id,
                    0,
                    0,
                    0,
                )
                if act_amounts_vary[j]:
                    act_patches.append((j, act_off + 20))
            elif at is PreserveTrigger:
                template[act_off : act_off + 32] = self._PRESERVE_TRIGGER_BYTES
            act_off += self._NUM_BYTES_PER_ACTION

        pe_sz = self._NUM_BYTES_PER_PE
        pe_base = conds_sz + self._ACTS_SECTION_SIZE
        pe_cache = self._fused_pe_bytes_cache
        pe_bytes = pe_cache.get(players0)
        if pe_bytes is None:
            pe_execution_cache = self._player_execution_cache
            pe = pe_execution_cache.get(players0)
            if pe is None:
                player_flags = [0] * 27
                for player_id in players0:
                    player_flags[player_id._id] = 1
                pe = DecodedPlayerExecution(
                    _execution_flags=0,
                    _player_flags=player_flags,
                    _current_action_index=0,
                )
                pe_execution_cache[players0] = pe
            buf = bytearray(pe_sz)
            pack_into_pe(
                buf, 0, pe._execution_flags, *pe._player_flags, pe._current_action_index
            )
            pe_bytes = bytes(buf)
            pe_cache[players0] = pe_bytes
        template[pe_base : pe_base + pe_sz] = pe_bytes

        fp_nz_pairs = tuple((i, b) for i, b in enumerate(template) if b)
        result = (fp_nz_pairs, bytes(template), tuple(cond_patches), tuple(act_patches))
        self._template_fingerprint_cache[fingerprint] = result
        return result

    def _fused_encode_to_bytes(
        self,
        rich_chk_section: RichTrigSection,
        context: RichChkEncodeContext,
    ) -> bytes:
        triggers = rich_chk_section.triggers
        trig_sz = self._NUM_BYTES_PER_TRIGGER
        total = len(triggers) * trig_sz

        if triggers:
            trig_id = id(triggers)
            template_info = self._template_cache.get(trig_id)
            if template_info is None:
                template_info = self._build_template_info(triggers)
                self._template_cache[trig_id] = template_info
            if template_info is not False:
                nz_pairs, template_bytes, cond_patches, act_patches = template_info
                n = len(triggers)
                # Zero-fill + strided writes: faster than template * n for sparse templates
                # because bytearray(N) uses calloc (near-zero cost for reused pages) while
                # template * n does a full 12 MB copy of mostly-zero content.
                if nz_pairs and len(nz_pairs) <= 64:
                    nz_key = (id(nz_pairs), n)
                    nz_bufs = self._nz_bufs_cache.get(nz_key)
                    if nz_bufs is None:
                        nz_bufs = [(pos, bytes([val]) * n) for pos, val in nz_pairs]
                        self._nz_bufs_cache[nz_key] = nz_bufs
                    data = bytearray(n * trig_sz)
                    for pos, buf in nz_bufs:
                        data[pos::trig_sz] = buf
                else:
                    data = bytearray(template_bytes * n)
                if cond_patches or act_patches:
                    if len(cond_patches) == 1 and not act_patches:
                        cond_idx, cond_off_rel = cond_patches[0]
                        amounts = [t._conditions[cond_idx]._amount for t in triggers]
                        amt = array.array("I", amounts)
                        if _IS_BIG_ENDIAN:
                            amt.byteswap()
                        ab = amt.tobytes()
                        data[cond_off_rel::trig_sz] = ab[0::4]
                        data[cond_off_rel + 1 :: trig_sz] = ab[1::4]
                        data[cond_off_rel + 2 :: trig_sz] = ab[2::4]
                        data[cond_off_rel + 3 :: trig_sz] = ab[3::4]
                    else:
                        for cond_idx, cond_off in cond_patches:
                            amounts = [
                                t._conditions[cond_idx]._amount for t in triggers
                            ]
                            amt = array.array("I", amounts)
                            if _IS_BIG_ENDIAN:
                                amt.byteswap()
                            ab = amt.tobytes()
                            data[cond_off::trig_sz] = ab[0::4]
                            data[cond_off + 1 :: trig_sz] = ab[1::4]
                            data[cond_off + 2 :: trig_sz] = ab[2::4]
                            data[cond_off + 3 :: trig_sz] = ab[3::4]
                        for act_idx, act_off in act_patches:
                            amounts = [t._actions[act_idx]._amount for t in triggers]
                            amt = array.array("I", amounts)
                            if _IS_BIG_ENDIAN:
                                amt.byteswap()
                            ab = amt.tobytes()
                            data[act_off::trig_sz] = ab[0::4]
                            data[act_off + 1 :: trig_sz] = ab[1::4]
                            data[act_off + 2 :: trig_sz] = ab[2::4]
                            data[act_off + 3 :: trig_sz] = ab[3::4]
                return data

        data = bytearray(total)
        pack_into_cond = self._COND_STRUCT.pack_into
        pack_into_act = self._ACT_STRUCT.pack_into
        pack_into_pe = self._PE_STRUCT.pack_into
        conds_sz = self._CONDS_SECTION_SIZE
        acts_sz = self._ACTS_SECTION_SIZE
        num_bytes_per_cond = self._NUM_BYTES_PER_CONDITION
        num_bytes_per_act = self._NUM_BYTES_PER_ACTION
        pe_sz = self._NUM_BYTES_PER_PE
        deaths_cid = self._DEATHS_CID
        set_deaths_aid = self._SET_DEATHS_AID
        preserve_bytes = self._PRESERVE_TRIGGER_BYTES
        preserve_type = PreserveTrigger
        deaths_type = DeathsCondition
        set_deaths_type = SetDeathsAction
        decoded_cond_type = DecodedTriggerCondition
        decoded_act_type = DecodedTriggerAction
        act_cache = self._action_type_cache
        cond_cache = self._condition_type_cache
        pe_cache = self._fused_pe_bytes_cache
        pe_execution_cache = self._player_execution_cache

        offset = 0
        for trigger in triggers:
            # --- conditions ---
            cond_off = offset
            for condition in trigger._conditions:
                c_type = type(condition)
                if c_type is deaths_type:
                    dc_cond = cast(DeathsCondition, condition)
                    f = dc_cond._flags
                    if f is _DEFAULT_TRIGGER_CONDITION_FLAGS:
                        flags_byte = 0
                    else:
                        flags_byte = (
                            int(f.unknown)
                            | (int(f.disabled) << 1)
                            | (int(f.always_display) << 2)
                            | (int(f.unit_properties_is_used) << 3)
                            | (int(f.unit_type_is_used) << 4)
                        )
                    pack_into_cond(
                        data,
                        cond_off,
                        0,
                        dc_cond._group._id,
                        dc_cond._amount,
                        dc_cond._unit._id,
                        dc_cond._comparator._id,
                        deaths_cid,
                        0,
                        flags_byte,
                        0,
                    )
                elif c_type is decoded_cond_type:
                    raw_cond = cast(DecodedTriggerCondition, condition)
                    pack_into_cond(
                        data,
                        cond_off,
                        raw_cond._location_id,
                        raw_cond._group,
                        raw_cond._quantity,
                        raw_cond._unit_id,
                        raw_cond._numeric_comparison_operation,
                        raw_cond._condition_id,
                        raw_cond._numeric_comparand_type,
                        raw_cond._flags,
                        raw_cond._mask_flag,
                    )
                else:
                    rich_cond = cast(RichTriggerCondition, condition)
                    transcoder = cond_cache.get(c_type)
                    if transcoder is None:
                        cid = rich_cond.condition_id()
                        if RichTriggerConditionTranscoderFactory.supports_transcoding_condition(
                            cid
                        ):
                            _f = RichTriggerConditionTranscoderFactory
                            transcoder = _f.make_rich_trigger_condition_transcoder(cid)
                            cond_cache[c_type] = transcoder
                        else:
                            raise ValueError(
                                f"No transcoder for condition type: {c_type}"
                            )
                    if rich_cond.flags is _DEFAULT_TRIGGER_CONDITION_FLAGS:
                        dc = transcoder._encode(rich_cond, context)
                    else:
                        dc = transcoder.encode(rich_cond, context)
                    pack_into_cond(
                        data,
                        cond_off,
                        dc._location_id,
                        dc._group,
                        dc._quantity,
                        dc._unit_id,
                        dc._numeric_comparison_operation,
                        dc._condition_id,
                        dc._numeric_comparand_type,
                        dc._flags,
                        dc._mask_flag,
                    )
                cond_off += num_bytes_per_cond

            # --- actions ---
            act_base = offset + conds_sz
            act_off = act_base
            for action in trigger._actions:
                a_type = type(action)
                if a_type is set_deaths_type:
                    sd_act = cast(SetDeathsAction, action)
                    fa = sd_act._flags
                    if fa is _DEFAULT_TRIGGER_ACTION_FLAGS:
                        flags_byte = 0
                    else:
                        flags_byte = (
                            int(fa.ignore_wait_or_transmission_once)
                            | (int(fa.disabled) << 1)
                            | (int(fa.always_display) << 2)
                            | (int(fa.unit_properties_is_used) << 3)
                            | (int(fa.unit_type_is_used) << 4)
                        )
                    pack_into_act(
                        data,
                        act_off,
                        0,
                        0,
                        0,
                        0,
                        sd_act._group._id,
                        sd_act._amount,
                        sd_act._unit._id,
                        set_deaths_aid,
                        sd_act._amount_modifier._id,
                        flags_byte,
                        0,
                        0,
                    )
                elif a_type is preserve_type:
                    data[act_off : act_off + 32] = preserve_bytes
                elif a_type is decoded_act_type:
                    raw_act = cast(DecodedTriggerAction, action)
                    pack_into_act(
                        data,
                        act_off,
                        raw_act._location_id,
                        raw_act._text_string_id,
                        raw_act._wav_string_id,
                        raw_act._time,
                        raw_act._first_group,
                        raw_act._second_group,
                        raw_act._action_argument_type,
                        raw_act._action_id,
                        raw_act._quantifier_or_switch_or_order,
                        raw_act._flags,
                        raw_act._padding,
                        raw_act._mask_flag,
                    )
                else:
                    rich_act = cast(RichTriggerAction, action)
                    transcoder = act_cache.get(a_type)
                    if transcoder is None:
                        aid = rich_act.action_id()
                        if RichTriggerActionTranscoderFactory.supports_transcoding_trig_action(
                            aid
                        ):
                            _af = RichTriggerActionTranscoderFactory
                            transcoder = _af.make_rich_trigger_action_transcoder(aid)
                            act_cache[a_type] = transcoder
                        else:
                            raise ValueError(f"No transcoder for action type: {a_type}")
                    if rich_act.flags is _DEFAULT_TRIGGER_ACTION_FLAGS:
                        da = transcoder._encode(rich_act, context)
                    else:
                        da = transcoder.encode(rich_act, context)
                    pack_into_act(
                        data,
                        act_off,
                        da._location_id,
                        da._text_string_id,
                        da._wav_string_id,
                        da._time,
                        da._first_group,
                        da._second_group,
                        da._action_argument_type,
                        da._action_id,
                        da._quantifier_or_switch_or_order,
                        da._flags,
                        da._padding,
                        da._mask_flag,
                    )
                act_off += num_bytes_per_act

            # --- player execution ---
            pe_base = act_base + acts_sz
            key = trigger._players
            pe_bytes = pe_cache.get(key)
            if pe_bytes is None:
                pe = pe_execution_cache.get(key)
                if pe is None:
                    player_flags = [0] * 27
                    for player_id in trigger._players:
                        player_flags[player_id._id] = 1
                    pe = DecodedPlayerExecution(
                        _execution_flags=0,
                        _player_flags=player_flags,
                        _current_action_index=0,
                    )
                    pe_execution_cache[key] = pe
                buf = bytearray(pe_sz)
                pack_into_pe(
                    buf,
                    0,
                    pe._execution_flags,
                    *pe._player_flags,
                    pe._current_action_index,
                )
                pe_bytes = bytes(buf)
                pe_cache[key] = pe_bytes
            data[pe_base : pe_base + pe_sz] = pe_bytes

            offset += trig_sz

        return data

    def _encode_trigger(
        self, rich_trigger: RichTrigger, rich_chk_encode_context: RichChkEncodeContext
    ) -> DecodedTrigger:
        conditions = self._encode_conditions(
            rich_trigger._conditions, rich_chk_encode_context
        )
        actions = self._encode_actions(rich_trigger._actions, rich_chk_encode_context)
        player_execution = self._encode_player_execution(rich_trigger._players)
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
