"""Represent the action byte of each mission briefing action."""

from ..richchk_enum import RichChkEnum


class BriefingActionId(RichChkEnum):
    NO_ACTION = (0, "NO_ACTION")
    WAIT = (1, "WAIT")
    PLAY_WAV = (2, "PLAY_WAV")
    TEXT_MESSAGE = (3, "TEXT_MESSAGE")
    MISSION_OBJECTIVES = (4, "MISSION_OBJECTIVES")
    SHOW_PORTRAIT = (5, "SHOW_PORTRAIT")
    HIDE_PORTRAIT = (6, "HIDE_PORTRAIT")
    DISPLAY_SPEAKING_PORTRAIT = (7, "DISPLAY_SPEAKING_PORTRAIT")
    TRANSMISSION = (8, "TRANSMISSION")
    SKIP_TUTORIAL_ENABLED = (9, "SKIP_TUTORIAL_ENABLED")
