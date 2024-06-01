"""TRIG - Triggers.  Player execution for a single trigger.

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
encountered with Action byte as 0
"""
import dataclasses


@dataclasses.dataclass(frozen=True)
class DecodedPlayerExecution:
    """Represent a decoded Player Execution structure.

    :param _execution_flags: u32 - Execution flags. Bit 0 - All conditions are met,
        executing actions, cleared on the next trigger loop. Bit 1 - Ignore the
        following actions: Defeat, Draw. Bit 2 - Preserve trigger. (Can replace Preserve
        Trigger action) Bit 3 - Ignore execution. Bit 4 - Ignore all of the following
        actions for this trigger until the next trigger loop: Wait, PauseGame,
        Transmission, PlayWAV, DisplayTextMessage, CenterView, MinimapPing,
        TalkingPortrait, and MuteUnitSpeech. Bit 5 - This trigger has paused the game,
        ignoring subsequent calls to Pause Game (Unpause Game clears this flag only in
        the same trigger), may automatically call unpause at the end of action
        execution? Bit 6 - Wait skipping disabled for this trigger, cleared on next
        trigger loop. Bit 7-31 - Unknown/unused
    :param _player_flags: u8[27] - 1 byte for each player in the #List of Players/Group
        IDs. 00 - Trigger is not executed for player. 01 - Trigger is executed for
        player.
    :param _current_action_index: u8 - Index of the current action, in StarCraft this is
        incremented after each action is executed, trigger execution ends when this is
        64 (Max Actions) or an action is encountered with Action byte as 0.
    """

    _execution_flags: int
    _player_flags: list[int]
    _current_action_index: int

    @property
    def execution_flags(self) -> int:
        """U32 - Execution flags."""
        return self._execution_flags

    @property
    def player_flags(self) -> list[int]:
        """U8[27] - 1 byte for each player in the #List of Players/Group IDs.

        00 - Trigger is not executed for player. 01 - Trigger is executed for player.
        """
        return self._player_flags

    @property
    def current_action_index(self) -> int:
        """U8 - Index of the current action, in StarCraft this is incremented after each
        action is executed, trigger execution ends when this is 64 (Max Actions) or an
        action is encountered with Action byte as 0."""
        return self._current_action_index
