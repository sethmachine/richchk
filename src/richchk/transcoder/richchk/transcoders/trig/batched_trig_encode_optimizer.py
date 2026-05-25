"""Batch/fused encoder for homogeneous TRIG trigger batches."""
import array
import collections
import struct
import sys
from typing import Any, ClassVar, Optional, cast

from .....model.chk.trig.decoded_player_execution import DecodedPlayerExecution
from .....model.chk.trig.decoded_trigger_action import DecodedTriggerAction
from .....model.chk.trig.decoded_trigger_condition import DecodedTriggerCondition
from .....model.richchk.richchk_encode_context import RichChkEncodeContext
from .....model.richchk.trig.actions.flags.trigger_action_flags import (
    _DEFAULT_TRIGGER_ACTION_FLAGS,
)
from .....model.richchk.trig.actions.preserve_trigger_action import PreserveTrigger
from .....model.richchk.trig.actions.set_deaths_action import SetDeathsAction
from .....model.richchk.trig.conditions.deaths_condition import DeathsCondition
from .....model.richchk.trig.conditions.flags.trigger_condition_flags import (
    _DEFAULT_TRIGGER_CONDITION_FLAGS,
)
from .....model.richchk.trig.rich_trig_section import RichTrigSection
from .....model.richchk.trig.rich_trigger_action import RichTriggerAction
from .....model.richchk.trig.rich_trigger_condition import RichTriggerCondition
from .rich_trigger_action_transcoder_factory import RichTriggerActionTranscoderFactory
from .rich_trigger_condition_transcoder_factory import (
    RichTriggerConditionTranscoderFactory,
)

_IS_BIG_ENDIAN: bool = sys.byteorder == "big"


class BatchedTrigEncodeOptimizer:
    """Encodes RichTrigSection to raw bytes using a batch/template strategy.

    For homogeneous trigger batches (same structure, only amounts vary), builds a binary
    template once and writes varying amounts via strided slice operations. Falls back to
    per-trigger packing for heterogeneous triggers.
    """

    _NUM_CONDITIONS_PER_TRIGGER = 16
    _NUM_ACTIONS_PER_TRIGGER = 64

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

    _DEATHS_CID: int = DeathsCondition.condition_id().id
    _SET_DEATHS_AID: int = SetDeathsAction.action_id().id
    _PRESERVE_AID: int = PreserveTrigger.action_id().id

    _PRESERVE_TRIGGER_BYTES: ClassVar[bytes] = struct.pack(
        "6I H 3B B H", 0, 0, 0, 0, 0, 0, 0, PreserveTrigger.action_id().id, 0, 0, 0, 0
    )
    _COND_STRUCT: ClassVar[struct.Struct] = struct.Struct(_CONDITION_FORMAT)
    _ACT_STRUCT: ClassVar[struct.Struct] = struct.Struct(_ACTION_FORMAT)
    _PE_STRUCT: ClassVar[struct.Struct] = struct.Struct(_PLAYER_EXECUTION_FORMAT)
    _I_STRUCT: ClassVar[struct.Struct] = struct.Struct("<I")

    _action_type_cache: ClassVar[dict[Any, Any]] = {}
    _condition_type_cache: ClassVar[dict[Any, Any]] = {}
    _fused_pe_bytes_cache: ClassVar[dict[Any, Any]] = {}
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
    _fused_bytes_cache: ClassVar[
        collections.OrderedDict[Any, Any]
    ] = collections.OrderedDict()  # (id(nz_pairs), n, hash(amounts_bytes)) → bytes
    _FUSED_BYTES_CACHE_MAX: ClassVar[int] = 16
    _player_execution_cache: ClassVar[dict[Any, Any]] = {}

    def encode(
        self,
        rich_chk_section: RichTrigSection,
        context: RichChkEncodeContext,
    ) -> bytes:
        if context.optimize:
            return self._fused_encode_to_bytes(rich_chk_section, context)
        return self._simple_encode_to_bytes(rich_chk_section, context)

    def get_secondary_cache_key(
        self, rich_chk_section: RichTrigSection
    ) -> Optional[tuple[Any, ...]]:
        """Returns a stable key for the secondary encode cache, or None if not
        applicable.

        The key is stable across fresh RichTrigSection objects that share the same
        structural fingerprint and amounts pattern.  Handles 1-cond-patch and
        1-cond+1-act-patch cases.
        """
        triggers = rich_chk_section.triggers
        if not triggers or rich_chk_section.cond0_amounts_bytes is None:
            return None
        trig_id = id(triggers)
        template_info = self._template_cache.get(trig_id)
        if template_info is None:
            return None
        if template_info is False:
            return None
        nz_pairs, _, cond_patches, act_patches = template_info
        if len(cond_patches) != 1:
            return None
        cond_idx, _ = cond_patches[0]
        if cond_idx != 0:
            return None
        n = len(triggers)
        nz_id = id(nz_pairs)
        if not act_patches:
            return (nz_id, n, rich_chk_section.cond0_amounts_hash)
        if len(act_patches) == 1:
            act_idx, _ = act_patches[0]
            if act_idx == 0 and rich_chk_section.act0_amounts_bytes is not None:
                combined = hash(
                    (
                        rich_chk_section.cond0_amounts_hash,
                        rich_chk_section.act0_amounts_hash,
                    )
                )
                return (nz_id, n, combined)
        return None

    @staticmethod
    def _compute_trigger_fingerprint(
        conds0: Any, acts0: Any, players0: Any
    ) -> tuple[Any, ...]:
        return (
            tuple((c.group, c.unit, c.comparator) for c in conds0),
            tuple(
                (a.group, a.unit, a.amount_modifier)
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
        conds0 = t0.conditions
        acts0 = t0.actions
        players0 = t0.players
        n_conds = len(conds0)
        n_acts = len(acts0)

        for c in conds0:
            if (
                type(c) is not DeathsCondition
                or c.flags is not _DEFAULT_TRIGGER_CONDITION_FLAGS
            ):
                return False
        for a in acts0:
            at = type(a)
            if at is SetDeathsAction:
                if a.flags is not _DEFAULT_TRIGGER_ACTION_FLAGS:
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
            if len(t.conditions) != n_conds or len(t.actions) != n_acts:
                return False
            if t.players != players0:
                return False
            for i in range(n_conds):
                c = t.conditions[i]
                c0 = conds0[i]
                if (
                    type(c) is not DeathsCondition
                    or c.flags is not _DEFAULT_TRIGGER_CONDITION_FLAGS
                    or c.group is not c0.group
                    or c.unit is not c0.unit
                    or c.comparator is not c0.comparator
                ):
                    return False
                if c.amount != c0.amount:
                    cond_amounts_vary[i] = True
            for j in range(n_acts):
                a = t.actions[j]
                a0 = acts0[j]
                at = type(a)
                if at is not type(a0):
                    return False
                if at is SetDeathsAction:
                    if (
                        a.flags is not _DEFAULT_TRIGGER_ACTION_FLAGS
                        or a.group is not a0.group
                        or a.unit is not a0.unit
                        or a.amount_modifier is not a0.amount_modifier
                    ):
                        return False
                    if a.amount != a0.amount:
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
            tmpl_amount = 0 if cond_amounts_vary[i] else c.amount
            pack_into_cond(
                template,
                cond_off,
                0,
                c.group.id,
                tmpl_amount,
                c.unit.id,
                c.comparator.id,
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
                tmpl_amount = 0 if act_amounts_vary[j] else a.amount
                pack_into_act(
                    template,
                    act_off,
                    0,
                    0,
                    0,
                    0,
                    a.group.id,
                    tmpl_amount,
                    a.unit.id,
                    set_deaths_aid,
                    a.amount_modifier.id,
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
                    player_flags[player_id.id] = 1
                pe = DecodedPlayerExecution(
                    _execution_flags=0,
                    _player_flags=player_flags,
                    _current_action_index=0,
                )
                pe_execution_cache[players0] = pe
            buf = bytearray(pe_sz)
            pack_into_pe(
                buf, 0, pe.execution_flags, *pe.player_flags, pe.current_action_index
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

        if triggers:
            trig_id = id(triggers)
            template_info = self._template_cache.get(trig_id)
            if template_info is None:
                template_info = self._build_template_info(triggers)
                self._template_cache[trig_id] = template_info
            if template_info is not False:
                nz_pairs, template_bytes, cond_patches, act_patches = template_info
                n = len(triggers)
                # Single-cond-patch fast path: compute amounts before allocation to
                # enable cache hit that skips the 12 MB bytearray + strided writes.
                if len(cond_patches) == 1 and not act_patches:
                    cond_idx, cond_off_rel = cond_patches[0]
                    if (
                        cond_idx == 0
                        and rich_chk_section.cond0_amounts_bytes is not None
                    ):
                        ab = rich_chk_section.cond0_amounts_bytes
                        ab_hash = rich_chk_section.cond0_amounts_hash
                    else:
                        amt = array.array(
                            "I", [t._conditions[cond_idx]._amount for t in triggers]
                        )
                        if _IS_BIG_ENDIAN:
                            amt.byteswap()
                        ab = amt.tobytes()
                        ab_hash = hash(ab)
                    nz_pairs_id = id(nz_pairs)
                    bytes_key = (nz_pairs_id, n, ab_hash)
                    cached_b = self._fused_bytes_cache.get(bytes_key)
                    if cached_b is not None:
                        return cast(bytes, cached_b)
                    nz_key = (nz_pairs_id, n)
                    nz_bufs = self._nz_bufs_cache.get(nz_key)
                    if nz_bufs is None:
                        nz_bufs = [(pos, bytes([val]) * n) for pos, val in nz_pairs]
                        self._nz_bufs_cache[nz_key] = nz_bufs
                    if nz_pairs and len(nz_pairs) <= 64:
                        data = bytearray(n * trig_sz)
                        for pos, buf in nz_bufs:
                            data[pos::trig_sz] = buf
                    else:
                        data = bytearray(template_bytes * n)
                    data[cond_off_rel::trig_sz] = ab[0::4]
                    data[cond_off_rel + 1 :: trig_sz] = ab[1::4]
                    data[cond_off_rel + 2 :: trig_sz] = ab[2::4]
                    data[cond_off_rel + 3 :: trig_sz] = ab[3::4]
                    fc = self._fused_bytes_cache
                    if len(fc) < self._FUSED_BYTES_CACHE_MAX:
                        result_b = bytes(data)
                        fc[bytes_key] = result_b
                        return result_b
                    return data
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
                    for cond_idx, cond_off in cond_patches:
                        if (
                            cond_idx == 0
                            and rich_chk_section.cond0_amounts_bytes is not None
                        ):
                            ab = rich_chk_section.cond0_amounts_bytes
                        else:
                            amt = array.array(
                                "I", [t._conditions[cond_idx]._amount for t in triggers]
                            )
                            if _IS_BIG_ENDIAN:
                                amt.byteswap()
                            ab = amt.tobytes()
                        data[cond_off::trig_sz] = ab[0::4]
                        data[cond_off + 1 :: trig_sz] = ab[1::4]
                        data[cond_off + 2 :: trig_sz] = ab[2::4]
                        data[cond_off + 3 :: trig_sz] = ab[3::4]
                    for act_idx, act_off in act_patches:
                        amt = array.array(
                            "I", [t._actions[act_idx]._amount for t in triggers]
                        )
                        if _IS_BIG_ENDIAN:
                            amt.byteswap()
                        ab = amt.tobytes()
                        data[act_off::trig_sz] = ab[0::4]
                        data[act_off + 1 :: trig_sz] = ab[1::4]
                        data[act_off + 2 :: trig_sz] = ab[2::4]
                        data[act_off + 3 :: trig_sz] = ab[3::4]
                return data

        return self._simple_encode_to_bytes(rich_chk_section, context)

    def _simple_encode_to_bytes(
        self,
        rich_chk_section: RichTrigSection,
        context: RichChkEncodeContext,
    ) -> bytes:
        triggers = rich_chk_section.triggers
        trig_sz = self._NUM_BYTES_PER_TRIGGER
        data = bytearray(len(triggers) * trig_sz)
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
            for condition in trigger.conditions:
                c_type = type(condition)
                if c_type is deaths_type:
                    dc_cond = cast(DeathsCondition, condition)
                    f = dc_cond.flags
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
                        dc_cond.group.id,
                        dc_cond.amount,
                        dc_cond.unit.id,
                        dc_cond.comparator.id,
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
                        raw_cond.location_id,
                        raw_cond.group,
                        raw_cond.quantity,
                        raw_cond.unit_id,
                        raw_cond.numeric_comparison_operation,
                        raw_cond.condition_id,
                        raw_cond.numeric_comparand_type,
                        raw_cond.flags,
                        raw_cond.mask_flag,
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
                        dc.location_id,
                        dc.group,
                        dc.quantity,
                        dc.unit_id,
                        dc.numeric_comparison_operation,
                        dc.condition_id,
                        dc.numeric_comparand_type,
                        dc.flags,
                        dc.mask_flag,
                    )
                cond_off += num_bytes_per_cond

            # --- actions ---
            act_base = offset + conds_sz
            act_off = act_base
            for action in trigger.actions:
                a_type = type(action)
                if a_type is set_deaths_type:
                    sd_act = cast(SetDeathsAction, action)
                    fa = sd_act.flags
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
                        sd_act.group.id,
                        sd_act.amount,
                        sd_act.unit.id,
                        set_deaths_aid,
                        sd_act.amount_modifier.id,
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
                        raw_act.location_id,
                        raw_act.text_string_id,
                        raw_act.wav_string_id,
                        raw_act.time,
                        raw_act.first_group,
                        raw_act.second_group,
                        raw_act.action_argument_type,
                        raw_act.action_id,
                        raw_act.quantifier_or_switch_or_order,
                        raw_act.flags,
                        raw_act.padding,
                        raw_act.mask_flag,
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
                        da.location_id,
                        da.text_string_id,
                        da.wav_string_id,
                        da.time,
                        da.first_group,
                        da.second_group,
                        da.action_argument_type,
                        da.action_id,
                        da.quantifier_or_switch_or_order,
                        da.flags,
                        da.padding,
                        da.mask_flag,
                    )
                act_off += num_bytes_per_act

            # --- player execution ---
            pe_base = act_base + acts_sz
            key = trigger.players
            pe_bytes = pe_cache.get(key)
            if pe_bytes is None:
                pe = pe_execution_cache.get(key)
                if pe is None:
                    player_flags = [0] * 27
                    for player_id in trigger.players:
                        player_flags[player_id.id] = 1
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
                    pe.execution_flags,
                    *pe.player_flags,
                    pe.current_action_index,
                )
                pe_bytes = bytes(buf)
                pe_cache[key] = pe_bytes
            data[pe_base : pe_base + pe_sz] = pe_bytes

            offset += trig_sz

        return data
