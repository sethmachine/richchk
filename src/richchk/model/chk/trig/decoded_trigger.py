""" "TRIG" - Triggers.Represent a single decoded trigger.

This section contains all the triggers in the map. This along with MBRF is the most
complicated section in the entire scenario.chk file as there is a lot of data packed
into too little of a space. Refer to the appendix at the bottom of this page for more
information. For easy reference, since each trigger contains 2400 bytes, the amount of
triggers can be gotten by taking the section length and dividing by 2400.

Every single trigger in the map will have the following format:

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

Player Execution Following the 16 conditions and 64 actions, every trigger also has this
structure

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
encountered with Action byte as 0

This section can be split. Additional TRIG sections will add more triggers.
"""

import dataclasses

from .decoded_player_execution import DecodedPlayerExecution
from .decoded_trigger_action import DecodedTriggerAction
from .decoded_trigger_condition import DecodedTriggerCondition


@dataclasses.dataclass(frozen=True)
class DecodedTrigger:
    """Represents a decoded trigger from the TRIG section.

    :param _conditions: Conditions of the trigger. 16 Conditions (20 byte struct) Every
        trigger has 16 of the following format, even if only one condition is used. See
        the appendix for information on which items are used for what conditions.
    :param _actions: Actions of the trigger. 64 Actions (32 byte struct) Immediately
        following the 16 conditions, there are 64 actions. There will always be 64 of
        the following structure, even if some of them are unused.
    :param _player_execution: Player execution of the trigger. Following the 16
        conditions and 64 actions, every trigger also has this structure.
    """

    _conditions: list[DecodedTriggerCondition]
    _actions: list[DecodedTriggerAction]
    _player_execution: DecodedPlayerExecution

    @property
    def conditions(self) -> list[DecodedTriggerCondition]:
        """Conditions of the trigger.

        16 Conditions (20 byte struct) Every trigger has 16 of the following format,
        even if only one condition is used. See the appendix for information on which
        items are used for what conditions.
        """
        return self._conditions

    @property
    def actions(self) -> list[DecodedTriggerAction]:
        """Actions of the trigger.

        64 Actions (32 byte struct) Immediately following the 16 conditions, there are
        64 actions. There will always be 64 of the following structure, even if some of
        them are unused.
        """
        return self._actions

    @property
    def player_execution(self) -> DecodedPlayerExecution:
        """Player execution of the trigger.

        Following the 16 conditions and 64 actions, every trigger also has this
        structure.
        """
        return self._player_execution
