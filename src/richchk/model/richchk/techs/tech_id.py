"""Represents each StarCraft technology's unique tech ID.

These are referenced throughout various CHK sections such as PTEC and TECS. Covers all
44 tech IDs (0-43); IDs 0-23 are classic, 24-43 are Brood War.
"""

from ..richchk_enum import RichChkEnum


class TechId(RichChkEnum):
    STIM_PACKS = (0, "Stim Packs")
    LOCKDOWN = (1, "Lockdown")
    EMP_SHOCKWAVE = (2, "EMP Shockwave")
    SPIDER_MINES = (3, "Spider Mines")
    SCANNER_SWEEP = (4, "Scanner Sweep")
    SIEGE_MODE = (5, "Siege Mode")
    DEFENSIVE_MATRIX = (6, "Defensive Matrix")
    IRRADIATE = (7, "Irradiate")
    YAMATO_GUN = (8, "Yamato Gun")
    CLOAKING_FIELD = (9, "Cloaking Field")
    PERSONNEL_CLOAKING = (10, "Personnel Cloaking")
    BURROWING = (11, "Burrowing")
    INFESTATION = (12, "Infestation")
    SPAWN_BROODLING = (13, "Spawn Broodling")
    DARK_SWARM = (14, "Dark Swarm")
    PLAGUE = (15, "Plague")
    CONSUME = (16, "Consume")
    ENSNARE = (17, "Ensnare")
    PARASITE = (18, "Parasite")
    PSIONIC_STORM = (19, "Psionic Storm")
    HALLUCINATION = (20, "Hallucination")
    RECALL = (21, "Recall")
    STASIS_FIELD = (22, "Stasis Field")
    ARCHON_WARP = (23, "Archon Warp")
    RESTORATION = (24, "Restoration")
    DISRUPTION_WEB = (25, "Disruption Web")
    MIND_CONTROL = (26, "Mind Control")
    DARK_ARCHON_MELD = (27, "Dark Archon Meld")
    FEEDBACK = (28, "Feedback")
    OPTICAL_FLARE = (29, "Optical Flare")
    MAELSTROM = (30, "Maelstrom")
    LURKER_ASPECT = (31, "Lurker Aspect")
    UNUSED_32 = (32, "Unused 32")
    HEALING = (33, "Healing")
    UNUSED_34 = (34, "Unused 34")
    UNUSED_35 = (35, "Unused 35")
    UNUSED_36 = (36, "Unused 36")
    UNUSED_37 = (37, "Unused 37")
    UNUSED_38 = (38, "Unused 38")
    UNUSED_39 = (39, "Unused 39")
    UNUSED_40 = (40, "Unused 40")
    UNUSED_41 = (41, "Unused 41")
    UNUSED_42 = (42, "Unused 42")
    UNUSED_43 = (43, "Unused 43")
