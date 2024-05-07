"""TRIG - Triggers.  Data structure for a single action.

64 Actions (32 byte struct)

Immediately following the 16 conditions, there are 64 actions. There will always be 64
of the following structure, even if some of them are unused.

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

Bit 4 - Unit type is used. Cleared in "Offset + Mask" EUD actions. Bit 5-7 -
Unknown/unused

u8: Padding

u16 (2 bytes): MaskFlag: set to "SC" (0x53, 0x43) when using the bitmask for EUDs, 0
otherwise
"""

import dataclasses


@dataclasses.dataclass(frozen=True)
class DecodedTriggerAction:
    """Represent a decoded Action from the TRIG section.

    :param _location_id: u32 - Source location in "Order" and "Move Unit", dest location
        in "Move Location" (1 based -- 0 refers to No Location), EUD Bitmask for a Death
        action if the MaskFlag is set to "SC".
    :param _text_string_id: u32 - String number for trigger text (0 means no string).
    :param _wav_string_id: u32 - WAV string number (0 means no string).
    :param _time: u32 - Seconds/milliseconds of time.
    :param _first_group: u32 - First (or only) Group/Player affected.
    :param _second_group: u32 - Second group affected, secondary location (1-based),
        CUWP #, number, AI script (4-byte string), switch (0-based #).
    :param _action_argument_type: u16 - Unit type, score type, resource type, alliance
        status.
    :param _action_id: u8 - Unique identifier for the signature and type of action.
    :param _quantifier_or_switch_or_order: u8 - Number of units (0 means All Units),
        action state, unit order, number modifier
    :param _flags: u8 - Flags (Bit 0 - Ignore a wait/transmission once, Bit 1 - Enabled
        flag, Bit 2 - Always display flag, Bit 3 - Unit properties is used, Bit 4 - Unit
        type is used, Bit 5-7 - Unknown/unused), Most of the time flags is either: * 100
        (4): used when displaying text messages to players * 10000 (16): whenever a
        "unit type" is used in the action * 0 (0): in all other cases it's 0
    :param _padding: u8 - just padding?.  This value is almost always 0.
    :param _mask_flag: u16 - MaskFlag (set to "SC" (0x53, 0x43) when using the bitmask
        for EUDs, 0 otherwise).
    """

    _location_id: int
    _text_string_id: int
    _wav_string_id: int
    _time: int
    _first_group: int
    _second_group: int
    _action_argument_type: int
    _action_id: int
    _quantifier_or_switch_or_order: int
    _flags: int
    _padding: int
    _mask_flag: int

    @property
    def location_id(self) -> int:
        """U32 - Source location in "Order" and "Move Unit", dest location in "Move
        Location" (1 based)."""
        return self._location_id

    @property
    def text_string_id(self) -> int:
        """U32 - String number for trigger text (0 means no string)."""
        return self._text_string_id

    @property
    def wav_string_id(self) -> int:
        """U32 - WAV string number (0 means no string)."""
        return self._wav_string_id

    @property
    def time(self) -> int:
        """U32 - Seconds/milliseconds of time."""
        return self._time

    @property
    def first_group(self) -> int:
        """U32 - First (or only) Group/Player affected."""
        return self._first_group

    @property
    def second_group(self) -> int:
        """U32 - Second group affected, secondary location (1-based), CUWP #, number, AI
        script (4-byte string), switch (0-based #)."""
        return self._second_group

    @property
    def action_argument_type(self) -> int:
        """U16 - Unit type, score type, resource type, alliance status."""
        return self._action_argument_type

    @property
    def action_id(self) -> int:
        """U8 - Action byte."""
        return self._action_id

    @property
    def quantifier_or_switch_or_order(self) -> int:
        """U8 - Number of units (0 means All Units), action state, unit order, number
        modifier."""
        return self._quantifier_or_switch_or_order

    @property
    def flags(self) -> int:
        """U8 - Flags (Bit 0 - Ignore a wait/transmission once, Bit 1 - Enabled flag,
        Bit 2 -

        Always display flag, Bit 3 - Unit properties is used, Bit 4 - Unit type is used,
        Bit 5-7 - Unknown/unused).
        """
        return self._flags

    @property
    def padding(self) -> int:
        """U8 - Padding."""
        return self._padding

    @property
    def mask_flag(self) -> int:
        """U16 - MaskFlag (set to "SC" (0x53, 0x43) when using the bitmask for EUDs, 0
        otherwise)."""
        return self._mask_flag
