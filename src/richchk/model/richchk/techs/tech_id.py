"""Represents each StarCraft technology's unique tech ID.

These are referenced throughout various CHK sections such as PTEC and TECS. Covers all
24 classic tech IDs (0-23).
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
