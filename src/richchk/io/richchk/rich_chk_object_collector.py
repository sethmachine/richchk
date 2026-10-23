"""Single-pass collector that gathers all tracked objects from a RichChk in one walk.

Replaces four independent recursive walkers (strings, locations, switches, cuwps) with a
single iterative traversal, cutting traversal cost by ~4x.
"""
import dataclasses
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

# Maps type → () for leaf/skip types, or tuple of fields for dataclasses.
# None means "not yet classified" (dict.get default).
# Pre-populate with concrete built-in scalars so first-encounter logic can
# immediately promote all-scalar dataclasses (like TriggerConditionFlags) to skip.
_SKIP: tuple[Any, ...] = ()
_EXPAND = object()  # marker: collection type — expand via stack.extend(obj)
_INITIAL_FIELDS_CACHE: dict[Type[Any], Any] = {
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
    fields_cache = dict(_INITIAL_FIELDS_CACHE)
    strings: OrderedDict[RichString, int] = OrderedDict()
    locations: set[RichLocation] = set()
    switches: set[RichSwitch] = set()
    cuwps: set[RichCuwpSlot] = set()

    for section in rich_chk.chk_sections:
        if not isinstance(section, RichChkSection):
            continue
        if isinstance(section, RichTrigSection):
            _collect_from_trig_section(
                section, strings, locations, switches, cuwps, fields_cache
            )
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
            fields_cache,
        )

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
    fields_cache: dict[Type[Any], Any],
) -> None:
    _walk(
        section,
        strings,
        locations,
        switches,
        cuwps,
        collect_locs,
        collect_swts,
        collect_cups,
        fields_cache,
    )


def _collect_from_trig_section(
    section: RichTrigSection,
    strings: "OrderedDict[RichString, int]",
    locations: "set[RichLocation]",
    switches: "set[RichSwitch]",
    cuwps: "set[RichCuwpSlot]",
    fields_cache: dict[Type[Any], Any],
) -> None:
    """Fast path for RichTrigSection: iterate conditions/actions directly, bypassing
    stack machinery for RichTrigger."""
    triggers = section._triggers
    cache = fields_cache
    _SKIP_ref = _SKIP
    n = len(triggers)
    if n == 0:
        return

    t0 = triggers[0]
    for item in t0._conditions:
        if cache.get(type(item)) is not _SKIP_ref:
            _walk(item, strings, locations, switches, cuwps, True, True, True, cache)
    for act in t0._actions:
        if cache.get(type(act)) is not _SKIP_ref:
            _walk(act, strings, locations, switches, cuwps, True, True, True, cache)

    if n == 1:
        return

    all_skip = all(cache.get(type(c)) is _SKIP_ref for c in t0._conditions) and all(
        cache.get(type(a)) is _SKIP_ref for a in t0._actions
    )

    if not all_skip:
        for t in triggers[1:]:
            for item in t._conditions:
                if cache.get(type(item)) is not _SKIP_ref:
                    _walk(
                        item,
                        strings,
                        locations,
                        switches,
                        cuwps,
                        True,
                        True,
                        True,
                        cache,
                    )
            for act in t._actions:
                if cache.get(type(act)) is not _SKIP_ref:
                    _walk(
                        act,
                        strings,
                        locations,
                        switches,
                        cuwps,
                        True,
                        True,
                        True,
                        cache,
                    )
        return

    t0_sig = t0._type_sig
    for t in triggers[1:]:
        if t._type_sig == t0_sig:
            continue
        for item in t._conditions:
            if cache.get(type(item)) is not _SKIP_ref:
                _walk(
                    item, strings, locations, switches, cuwps, True, True, True, cache
                )
        for act in t._actions:
            if cache.get(type(act)) is not _SKIP_ref:
                _walk(act, strings, locations, switches, cuwps, True, True, True, cache)


def _walk(
    root: object,
    strings: "OrderedDict[RichString, int]",
    locations: "set[RichLocation]",
    switches: "set[RichSwitch]",
    cuwps: "set[RichCuwpSlot]",
    collect_locs: bool,
    collect_swts: bool,
    collect_cups: bool,
    fields_cache: dict[Type[Any], Any],
) -> None:
    stack = [root]
    while stack:
        obj = stack.pop()
        obj_type = type(obj)

        # Fast path: previously classified type.
        cached = fields_cache.get(obj_type)
        if cached is not None:
            if cached is _SKIP:
                continue
            if cached is _EXPAND:
                for item in obj:  # type: ignore[attr-defined]
                    if fields_cache.get(type(item)) is not _SKIP:
                        stack.append(item)
                continue
            # cached is a tuple of field name strings — inline-expand collections
            pushed_any = False
            has_expand_field = False
            for name in cached:
                val = getattr(obj, name)
                val_cached = fields_cache.get(type(val))
                if val_cached is _SKIP:
                    continue
                if val_cached is _EXPAND:
                    has_expand_field = True
                    for item in val:
                        ic = fields_cache.get(type(item))
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
                fields_cache[obj_type] = _SKIP
            continue

        # First encounter: classify this type.

        # RichString always handled specially — never cache this type
        if isinstance(obj, RichString):
            if not isinstance(obj, RichNullString):
                strings[obj] = 0
            continue

        # Leaf / scalar types: mark as skip immediately
        if isinstance(obj, _LEAF_TYPES):
            fields_cache[obj_type] = _SKIP
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
            fields = dataclasses.fields(obj)
            to_push = []
            for f in fields:
                val = getattr(obj, f.name)
                val_cached = fields_cache.get(type(val))
                if val_cached is None or val_cached:
                    to_push.append(val)
            if not isinstance(obj, (RichLocation, RichSwitch, RichCuwpSlot)):
                # Only cache types with stable walk-all-fields behaviour.
                # If nothing needed visiting, mark as skip immediately.
                # Store field names (strings) instead of Field objects for faster access.
                if to_push or not fields:
                    fields_cache[obj_type] = tuple(f.name for f in fields)
                else:
                    fields_cache[obj_type] = _SKIP
            stack.extend(to_push)
            continue
