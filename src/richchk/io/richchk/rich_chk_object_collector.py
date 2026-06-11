"""Single-pass collector that gathers all tracked objects from a RichChk in one walk.

Replaces four independent recursive walkers (strings, locations, switches, cuwps) with a
single iterative traversal, cutting traversal cost by ~4x.
"""
import dataclasses
import weakref
from collections import OrderedDict
from enum import Enum
from typing import Any, Tuple, Type

from ...model.richchk.mrgn.rich_location import RichLocation
from ...model.richchk.mrgn.rich_mrgn_section import RichMrgnSection
from ...model.richchk.rich_chk import RichChk
from ...model.richchk.rich_chk_section import RichChkSection
from ...model.richchk.str.rich_string import RichNullString, RichString
from ...model.richchk.swnm.rich_switch import RichSwitch
from ...model.richchk.swnm.rich_swnm_section import RichSwnmSection
from ...model.richchk.trig.rich_trig_section import RichTrigSection
from ...model.richchk.uprp.rich_cuwp_slot import RichCuwpSlot
from ...model.richchk.uprp.rich_uprp_section import RichUprpSection

_LEAF_TYPES = (Enum, int, bool, str, type(None), bytes, bytearray, float, type)

_trig_triggers_no_collectibles: dict[
    Any, Any
] = (
    {}
)  # id(section._triggers) → triggers_ref (identity-verified; cleaned via finalizer)
_collect_cache: dict[
    Any, Any
] = {}  # id(rich_chk) → (rich_chk_ref, strings, locations, switches, cuwps)
_section_collectibles_cache: dict[
    Any, Any
] = {}  # id(section) → (section_ref, strings_list, locs, swts, cuwps, cl, cs, cc)
_no_collectibles_type_sigs: set[
    Any
] = set()  # type_sig tuples confirmed to have no collectibles


# Maps type → () for leaf/skip types, or tuple of fields for dataclasses.
# None means "not yet classified" (dict.get default).
# Pre-populate with concrete built-in scalars so first-encounter logic can
# immediately promote all-scalar dataclasses (like TriggerConditionFlags) to skip.
_SKIP: tuple[Any, ...] = ()
_EXPAND = object()  # marker: collection type — expand via stack.extend(obj)
# Cache dataclasses.fields() results per type to avoid repeated introspection.
_dc_fields_cache: dict[Any, Any] = {}
_fields_cache: dict[Type[Any], Any] = {
    int: _SKIP,
    bool: _SKIP,
    str: _SKIP,
    float: _SKIP,
    type(None): _SKIP,
    bytes: _SKIP,
    bytearray: _SKIP,
    list: _EXPAND,
    tuple: _EXPAND,
    set: _EXPAND,
    frozenset: _EXPAND,
}


def collect_rich_objects(
    rich_chk: RichChk,
) -> Tuple[
    "OrderedDict[RichString, int]",
    "set[RichLocation]",
    "set[RichSwitch]",
    "set[RichCuwpSlot]",
]:
    """Walk all RichChkSection objects once, collecting:

    - strings: OrderedDict[RichString, int] — all non-null RichString values (all
    sections) - locations: set[RichLocation] — RichLocations found outside
    RichMrgnSection - switches: set[RichSwitch] — RichSwitch found outside
    RichSwnmSection - cuwps: set[RichCuwpSlot] — RichCuwpSlot found outside
    RichUprpSection
    """
    chk_id = id(rich_chk)
    cached = _collect_cache.get(chk_id)
    if cached is not None:
        ref_obj = cached[0]()
        if ref_obj is rich_chk:
            return cached[1], cached[2], cached[3], cached[4]
        else:
            del _collect_cache[chk_id]

    strings: OrderedDict[RichString, int] = OrderedDict()
    locations: set[RichLocation] = set()
    switches: set[RichSwitch] = set()
    cuwps: set[RichCuwpSlot] = set()

    for section in rich_chk.chk_sections:
        if not isinstance(section, RichChkSection):
            continue
        if isinstance(section, RichTrigSection):
            _collect_from_trig_section(section, strings, locations, switches, cuwps)
            continue
        collect_locs = not isinstance(section, RichMrgnSection)
        collect_swts = not isinstance(section, RichSwnmSection)
        collect_cups = not isinstance(section, RichUprpSection)
        _collect_non_trig_section(
            section,
            strings,
            locations,
            switches,
            cuwps,
            collect_locs,
            collect_swts,
            collect_cups,
        )

    _wr = weakref.ref(rich_chk, lambda _: _collect_cache.pop(chk_id, None))
    _collect_cache[chk_id] = (_wr, strings, locations, switches, cuwps)
    return strings, locations, switches, cuwps


def _collect_non_trig_section(
    section: RichChkSection,
    strings: "OrderedDict[RichString, int]",
    locations: "set[RichLocation]",
    switches: "set[RichSwitch]",
    cuwps: "set[RichCuwpSlot]",
    collect_locs: bool,
    collect_swts: bool,
    collect_cups: bool,
) -> None:
    sec_id = id(section)
    cached = _section_collectibles_cache.get(sec_id)
    if (
        cached is not None
        and cached[0] is section
        and cached[5] == collect_locs
        and cached[6] == collect_swts
        and cached[7] == collect_cups
    ):
        for s in cached[1]:
            strings[s] = 0
        locations.update(cached[2])
        switches.update(cached[3])
        cuwps.update(cached[4])
        return
    sec_strings: OrderedDict[RichString, int] = OrderedDict()
    sec_locs: set[RichLocation] = set()
    sec_swts: set[RichSwitch] = set()
    sec_cuwps: set[RichCuwpSlot] = set()
    _walk(
        section,
        sec_strings,
        sec_locs,
        sec_swts,
        sec_cuwps,
        collect_locs,
        collect_swts,
        collect_cups,
    )
    _section_collectibles_cache[sec_id] = (
        section,
        list(sec_strings.keys()),
        sec_locs,
        sec_swts,
        sec_cuwps,
        collect_locs,
        collect_swts,
        collect_cups,
    )
    for s in sec_strings.keys():
        strings[s] = 0
    locations.update(sec_locs)
    switches.update(sec_swts)
    cuwps.update(sec_cuwps)


def _collect_from_trig_section(
    section: RichTrigSection,
    strings: "OrderedDict[RichString, int]",
    locations: "set[RichLocation]",
    switches: "set[RichSwitch]",
    cuwps: "set[RichCuwpSlot]",
) -> None:
    """Fast path for RichTrigSection: iterate conditions/actions directly, bypassing
    stack machinery for RichTrigger."""
    triggers = section._triggers
    trig_list_id = id(triggers)
    cached_ref = _trig_triggers_no_collectibles.get(trig_list_id)
    if cached_ref is not None and cached_ref is triggers:
        return
    cache = _fields_cache
    _SKIP_ref = _SKIP
    found_any = False
    n = len(triggers)
    if n == 0:
        _trig_triggers_no_collectibles[trig_list_id] = triggers
        weakref.finalize(
            section, _trig_triggers_no_collectibles.pop, trig_list_id, None
        )
        return

    # Process trigger[0] to ensure all its types are in _fields_cache.
    t0 = triggers[0]
    for item in t0._conditions:
        if cache.get(type(item)) is not _SKIP_ref:
            _walk(item, strings, locations, switches, cuwps, True, True, True)
            found_any = True
    for act in t0._actions:
        if cache.get(type(act)) is not _SKIP_ref:
            _walk(act, strings, locations, switches, cuwps, True, True, True)
            found_any = True

    if n == 1:
        if not found_any:
            _trig_triggers_no_collectibles[trig_list_id] = triggers
        return

    # Determine if fast _type_sig path is valid: all types in t0 must be _SKIP after warmup.
    # found_any=False means they were already _SKIP before; True means _walk was called and
    # may have promoted some to _SKIP or left them as tuple(field_names).
    if found_any:
        all_skip = all(cache.get(type(c)) is _SKIP_ref for c in t0._conditions) and all(
            cache.get(type(a)) is _SKIP_ref for a in t0._actions
        )
    else:
        all_skip = True

    if not all_skip:
        for t in triggers[1:]:
            for item in t._conditions:
                if cache.get(type(item)) is not _SKIP_ref:
                    _walk(item, strings, locations, switches, cuwps, True, True, True)
                    found_any = True
            for act in t._actions:
                if cache.get(type(act)) is not _SKIP_ref:
                    _walk(act, strings, locations, switches, cuwps, True, True, True)
                    found_any = True
        if not found_any:
            _trig_triggers_no_collectibles[trig_list_id] = triggers
        return

    # Fast path: all types in t0 are _SKIP → use pre-computed _type_sig tuple for remaining.
    # t0._type_sig = (type(c0), ..., type(a0), ...) — pre-computed in RichTrigger.__post_init__.
    # Tuple equality is a single C-level comparison vs. multiple Python-level type() is checks.
    t0_sig = t0._type_sig

    # If this type signature was already confirmed clean on a prior list, skip the entire loop.
    if t0_sig in _no_collectibles_type_sigs:
        _trig_triggers_no_collectibles[trig_list_id] = triggers
        weakref.finalize(
            section, _trig_triggers_no_collectibles.pop, trig_list_id, None
        )
        return

    all_same_sig = True
    for t in triggers[1:]:
        if t._type_sig == t0_sig:
            continue
        all_same_sig = False
        tc = t._conditions
        ta = t._actions
        for item in tc:
            if cache.get(type(item)) is not _SKIP_ref:
                _walk(item, strings, locations, switches, cuwps, True, True, True)
                found_any = True
        for act in ta:
            if cache.get(type(act)) is not _SKIP_ref:
                _walk(act, strings, locations, switches, cuwps, True, True, True)
                found_any = True

    if not found_any:
        if all_same_sig:
            _no_collectibles_type_sigs.add(t0_sig)
        _trig_triggers_no_collectibles[trig_list_id] = triggers
        weakref.finalize(
            section, _trig_triggers_no_collectibles.pop, trig_list_id, None
        )


def _walk(
    root: object,
    strings: "OrderedDict[RichString, int]",
    locations: "set[RichLocation]",
    switches: "set[RichSwitch]",
    cuwps: "set[RichCuwpSlot]",
    collect_locs: bool,
    collect_swts: bool,
    collect_cups: bool,
) -> None:
    stack = [root]
    while stack:
        obj = stack.pop()
        obj_type = type(obj)

        # Fast path: previously classified type.
        cached = _fields_cache.get(obj_type)
        if cached is not None:
            if cached is _SKIP:
                continue
            if cached is _EXPAND:
                for item in obj:  # type: ignore[attr-defined]
                    if _fields_cache.get(type(item)) is not _SKIP:
                        stack.append(item)
                continue
            # cached is a tuple of field name strings — inline-expand collections
            pushed_any = False
            has_expand_field = False
            for name in cached:
                val = getattr(obj, name)
                val_cached = _fields_cache.get(type(val))
                if val_cached is _SKIP:
                    continue
                if val_cached is _EXPAND:
                    has_expand_field = True
                    for item in val:
                        ic = _fields_cache.get(type(item))
                        if ic is None or ic:
                            stack.append(item)
                            pushed_any = True
                else:
                    stack.append(val)
                    pushed_any = True
            # Auto-promote only for types with no collection fields; types with
            # collections (e.g. RichTrigger) may have different item types across
            # instances so are never promoted to SKIP.
            if not pushed_any and not has_expand_field and cached:
                _fields_cache[obj_type] = _SKIP
            continue

        # First encounter: classify this type.

        # RichString always handled specially — never cache this type
        if isinstance(obj, RichString):
            if not isinstance(obj, RichNullString):
                strings[obj] = 0
            continue

        # Leaf / scalar types: mark as skip immediately
        if isinstance(obj, _LEAF_TYPES):
            _fields_cache[obj_type] = _SKIP
            continue

        # Collection-flag-sensitive special types: never cache
        if isinstance(obj, RichLocation):
            if collect_locs:
                locations.add(obj)
                stack.append(obj._custom_location_name)
                continue
            # collect_locs=False: walk fields (to find strings etc.) but don't cache
        elif isinstance(obj, RichSwitch):
            if collect_swts:
                switches.add(obj)
                stack.append(obj._custom_name)
                continue
        elif isinstance(obj, RichCuwpSlot):
            if collect_cups:
                cuwps.add(obj)
                continue
        elif isinstance(obj, (list, tuple)):
            stack.extend(obj)
            continue
        elif isinstance(obj, set):
            stack.extend(obj)
            continue
        elif isinstance(obj, dict):
            stack.extend(obj.keys())
            stack.extend(obj.values())
            continue

        if dataclasses.is_dataclass(obj):
            fields = _dc_fields_cache.get(obj_type)
            if fields is None:
                fields = dataclasses.fields(obj)
                _dc_fields_cache[obj_type] = fields
            to_push = []
            for f in fields:
                val = getattr(obj, f.name)
                val_cached = _fields_cache.get(type(val))
                if val_cached is None or val_cached:
                    to_push.append(val)
            if not isinstance(obj, (RichLocation, RichSwitch, RichCuwpSlot)):
                # Only cache types with stable walk-all-fields behaviour.
                # If nothing needed visiting, mark as skip immediately.
                # Store field names (strings) instead of Field objects for faster access.
                if to_push or not fields:
                    _fields_cache[obj_type] = tuple(f.name for f in fields)
                else:
                    _fields_cache[obj_type] = _SKIP
            stack.extend(to_push)
            continue
