# RichChk — CLAUDE.md

## Project Overview

RichChk is a Python library for parsing, editing, and writing StarCraft map files (.SCM/.SCX). It converts the binary CHK format (the scenario data embedded inside a StarCraft MPQ archive) into rich, human-readable Python dataclasses that can be safely modified and written back to a playable map file.

The library never modifies files in place — every edit produces a new object. Unknown CHK sections are preserved as opaque binary blobs so the library degrades gracefully on partially-supported formats.

## Running Tests

```bash
pytest test/
```

Tests use pytest with fixtures defined in `test/conftest.py`. Individual test files mirror the `src/` directory layout.

## Directory Structure

```
src/richchk/
├── model/
│   ├── chk/          # Low-level decoded binary section dataclasses
│   └── richchk/      # Rich human-readable section dataclasses
├── transcoder/
│   ├── chk/          # Binary ↔ DecodedChk transcoders (struct.pack/unpack)
│   └── richchk/      # DecodedChk ↔ RichChk transcoders
├── editor/
│   ├── chk/          # Raw CHK section editors
│   └── richchk/      # Rich section editors (RichChkEditor, RichTrigEditor, etc.)
├── io/
│   ├── chk/          # ChkIo: raw CHK binary file I/O
│   ├── richchk/      # RichChkIo: CHK I/O with transcoding
│   └── mpq/          # StarCraftMpqIo: reads/writes CHK inside .SCX/.SCM files
├── mpq/              # StormLib DLL bindings for MPQ archive access
├── config/           # YAML-based logging configuration
└── util/             # Logger and dataclass helpers
test/                 # Mirrors src/ layout; pytest fixtures in conftest.py
examples/             # hello_world.py, hyper_triggers.py — end-to-end usage
```

## Coding Conventions

- **Immutable frozen dataclasses** everywhere: `@dataclasses.dataclass(frozen=True)`. Never mutate objects; return new ones.
- **Full static typing** enforced by mypy. Always annotate parameters and return types.
- **Functional style**: editors accept a section and return a new section; they do not hold mutable state.
- **No null**: use `Optional[T]` and explicit `None` checks rather than sentinel values.
- **Enums** for CHK section names (`ChkSectionName`), unit IDs (`UnitId`), player IDs (`PlayerId`), weapon IDs (`WeaponId`), trigger action/condition types, etc.
- **Protocols** (`typing.Protocol`) for transcoder interfaces rather than abstract base classes.
- **`@functools.cached_property`** for expensive derived values on dataclasses.
- Pre-commit hooks enforce black, isort, flake8, docformatter, and mypy — run `pre-commit run --all-files` before committing.

## Key Classes

| Class | Location | Role |
|---|---|---|
| `RichChk` | `model/richchk/rich_chk.py` | Root container; ordered list of rich + raw sections |
| `DecodedChk` | `model/chk/decoded_chk.py` | Container of decoded binary CHK sections |
| `ChkSectionName` | `model/chk_section_name.py` | Enum of all CHK section identifiers |
| `RichChkEditor` | `editor/richchk/rich_chk_editor.py` | Replace/add/remove sections in a `RichChk` |
| `RichTrigEditor` | `editor/richchk/rich_trig_editor.py` | Add `RichTrigger` objects to the TRIG section |
| `RichUnixEditor` | `editor/richchk/rich_unix_editor.py` | Upsert unit settings in the UNIX section |
| `RichMrgnEditor` | `editor/richchk/rich_mrgn_editor.py` | Add/replace locations in the MRGN section |
| `ChkIo` | `io/chk/chk_io.py` | Read/write raw CHK binary streams |
| `RichChkIo` | `io/richchk/rich_chk_io.py` | CHK I/O with full transcoding |
| `StarCraftMpqIo` | `io/mpq/starcraft_mpq_io.py` | Read/write CHK inside a .SCX/.SCM MPQ archive |
| `ChkQueryUtil` | (util) | `find_only_rich_section_in_chk(SectionType, chk)` |
| `MrgnQueryUtil` | (util) | `find_location_by_name(name, mrgn)` |

## Typical Map Editing Workflow

```python
from richchk.io.mpq.starcraft_mpq_io_helper import StarCraftMpqIoHelper
from richchk.editor.richchk.rich_chk_editor import RichChkEditor
from richchk.editor.richchk.rich_trig_editor import RichTrigEditor
from richchk.editor.richchk.rich_unix_editor import RichUnixEditor
from richchk.model.richchk.trig.rich_trig_section import RichTrigSection
from richchk.model.richchk.unix.rich_unix_section import RichUnixSection
from richchk.util.richchk.rich_chk_query_util import ChkQueryUtil

mpqio = StarCraftMpqIoHelper.create_mpq_io()
chk = mpqio.read_chk_from_mpq(input_map_path)

# Edit triggers
trig_section = ChkQueryUtil.find_only_rich_section_in_chk(RichTrigSection, chk)
new_trig = RichTrigEditor.add_triggers(my_triggers, trig_section)
chk = RichChkEditor().replace_chk_section(new_trig, chk)

# Edit unit settings
unix_section = ChkQueryUtil.find_only_rich_section_in_chk(RichUnixSection, chk)
new_unix = RichUnixEditor().upsert_all_unit_settings(my_unit_settings, unix_section)
chk = RichChkEditor().replace_chk_section(new_unix, chk)

mpqio.save_chk_to_mpq(chk, input_map_path, output_map_path, overwrite_existing=False)
```

Always write to a **new file** (`overwrite_existing=False`). Treat existing maps as immutable inputs.

## Triggers

A `RichTrigger` has conditions, actions, and a set of player owners:

```python
from richchk.model.richchk.trig.rich_trigger import RichTrigger
from richchk.model.richchk.trig.player_id import PlayerId
from richchk.model.richchk.trig.conditions.deaths_condition import DeathsCondition
from richchk.model.richchk.trig.actions.set_deaths_action import SetDeathsAction
from richchk.model.richchk.trig.actions.preserve_trigger import PreserveTrigger

trigger = RichTrigger(
    _conditions=[DeathsCondition(_group=PlayerId.PLAYER_8, _unit=UnitId.ZERG_SCOURGE,
                                  _comparator=NumericComparator.AT_LEAST, _amount=1)],
    _actions=[SetDeathsAction(...), PreserveTrigger()],
    _players={PlayerId.PLAYER_1},
)
```

`PreserveTrigger()` must be the **last action** to make a trigger repeat each game cycle.

Condition ordering matters for performance: `DeathsCondition` (cheapest) should come before `BringCondition` (most expensive — scans all units on the map).

## Unit Settings

```python
from richchk.model.richchk.unis.unit_setting import UnitSetting
from richchk.model.richchk.unis.weapon_setting import WeaponSetting

UnitSetting(
    _unit_id=UnitId.PROTOSS_ZEALOT,
    _hitpoints=Decimal("600"),
    _shieldpoints=0,
    _armorpoints=0,
    _build_time=1,
    _mineral_cost=1,
    _gas_cost=1,
    _custom_unit_name=RichString(_value="Footman"),
    _weapons=[WeaponSetting(_weapon_id=WeaponId.PSI_BLADES_NORMAL, _base_damage=5, _upgrade_damage=1)],
)
```

Apply in bulk with `RichUnixEditor().upsert_all_unit_settings(settings_list, unix_section)`.

## Locations (MRGN)

Locations are rectangles defined by pixel coordinates. Look them up by name at build time:

```python
from richchk.util.richchk.rich_mrgn_query_util import MrgnQueryUtil
from richchk.model.richchk.mrgn.rich_mrgn_section import RichMrgnSection

mrgn = ChkQueryUtil.find_only_rich_section_in_chk(RichMrgnSection, chk)
location = MrgnQueryUtil.find_location_by_name("my-location-name", mrgn)
```

A `RichLocation` has `left`, `top`, `right`, `bottom` pixel coordinates and an optional `name`.

## Adding a New CHK Section

Follow this four-step pattern:

**1. Model layer** — create two frozen dataclasses:
- `src/richchk/model/chk/<section>/decoded_<section>_section.py` — inherits `DecodedChkSection`
- `src/richchk/model/richchk/<section>/rich_<section>_section.py` — inherits `RichChkSection`

**2. Binary transcoder** — `src/richchk/transcoder/chk/transcoders/chk_<section>_transcoder.py`:
- Implements `ChkSectionTranscoder` protocol
- `decode(data: bytes) -> DecodedXSection` using `struct.unpack`
- `_encode(section: DecodedXSection) -> bytes` using `struct.pack`
- Register in `ChkSectionTranscoderFactory` via `_RegistrableTranscoder`

**3. Rich transcoder** — `src/richchk/transcoder/richchk/transcoders/richchk_<section>_transcoder.py`:
- Implements `RichChkSectionTranscoder` protocol
- `decode(decoded: DecodedXSection) -> RichXSection`
- `encode(rich: RichXSection) -> DecodedXSection`
- Register in `RichChkSectionTranscoderFactory`

**4. Editor** (if needed) — `src/richchk/editor/richchk/rich_<section>_editor.py`:
- Pure functions; accept a section and return a new section

**5. Tests** — add round-trip tests:
- Binary → decoded → binary should equal original
- Decoded → rich → decoded should equal original

## Dependencies

Defined in `pyproject.toml`. Key runtime deps:
- `PyYAML` — YAML config parsing
- `mutagen` — WAV audio file metadata
- `dataclass-wizard` — dataclass serialization helpers

StormLib is a native DLL dependency (not a Python package) — required only for MPQ I/O. Pre-built DLLs are bundled for Windows x64, macOS Apple Silicon, and Linux x64, but bring your own for production use.
