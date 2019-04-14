"""Maps each unit ID to corresponding weapon ID(s).

"""

from .unit_ids import *
from .weapon_ids import *

PRIMARY = 0
SECONDARY = 1

UNIT_TO_WEAPON = {
    TERRAN_MARINE: [GAUSS_RIFLE_NORMAL],
    TERRAN_GHOST: [C10_CONCUSSION_RIFLE_NORMAL],
    TERRAN_VULTURE: [FRAGMENTATION_GRENADE_NORMAL],
    TERRAN_GOLIATH: [TWIN_AUTOCANNONS_NORMAL, HELLFIRE_MISSILE_PACK_NORMAL],
    GOLIATH_TURRET: [HELLFIRE_MISSILE_PACK_NORMAL],
    TERRAN_SIEGE_TANK_TANK_MODE: [ARCLITE_CANNON_NORMAL],
    TANK_TURRET_TANK_MODE: [ARCLITE_CANNON_NORMAL],
    TERRAN_SCV: [FUSION_CUTTER],
    TERRAN_WRAITH: [BURST_LASERS_NORMAL, GEMINI_MISSILES_NORMAL],
    GUI_MONTANG_FIREBAT: [FLAME_THROWER_GUI_MONTAG],
    TERRAN_BATTLECRUISER: [ATS_LASER_BATTERY_NORMAL, ATA_LASER_BATTERY_NORMAL],
    VULTURE_SPIDER_MINE: [SPIDER_MINES],
    NUCLEAR_MISSILE: [NUCLEAR_MISSILE_WEAPON],
    SARAH_KERRIGAN_GHOST: [C10_CONCUSSION_RIFLE_SARAH_KERRIGAN],
    ALAN_SCHEZAR_GOLIATH: [TWIN_AUTOCANNONS_ALAN_SCHEZAR, HELLFIRE_MISSILE_PACK_ALAN_SCHEZAR],
    ALAN_SCHEZAR_TURRET: [TWIN_AUTOCANNONS_ALAN_SCHEZAR],
    JIM_RAYNOR_MARINE: [GAUSS_RIFLE_JIM_RAYNORMARINE],
    JIM_RAYNOR_VULTURE: [FRAGMENTATION_GRENADE_JIM_RAYNORVULTURE],
    TOM_KAZANSKY_WRAITH: [BURST_LASERS_TOM_KAZANSKY, GEMINI_MISSILES_TOM_KAZANSKY],
    EDMUND_DUKE_SIEGE_TANK: [ARCLITE_CANNON_EDMUND_DUKE],
    EDMUND_DUKE_TURRET: [ARCLITE_CANNON_EDMUND_DUKE],
    EDMUND_DUKE_SIEGE_MODE: [ARCLITE_SHOCK_CANNON_EDMUND_DUKE],
    EDMUND_DUKE_TURRET_SIEGE_MODE: [ARCLITE_SHOCK_CANNON_EDMUND_DUKE],
    HYPERION_BATTLECRUISER: [ATS_LASER_BATTERY_HYPERION, ATA_LASER_BATTERY_HYPERION],
    NORAD_II_BATTLECRUISER: [ATS_LASER_BATTERY_NORAD_II_MENGSK_DUGALLE, ATA_LASER_BATTERY_NORAD_II_MENGSK_DUGALLE],
    TERRAN_SIEGE_TANK_SIEGE_MODE: [ARCLITE_SHOCK_CANNON_NORMAL],
    TANK_TURRET_SIEGE_MODE: [ARCLITE_SHOCK_CANNON_NORMAL],
    FIREBAT: [FLAME_THROWER_NORMAL],
    ZERG_ZERGLING: [CLAWS_NORMAL],
    ZERG_HYDRALISK: [NEEDLE_SPINES_NORMAL],
    ZERG_ULTRALISK: [KAISER_BLADES_NORMAL],
    ZERG_BROODLING: [TOXIC_SPORES_BROODLING],
    ZERG_DRONE: [SPINES],
    ZERG_MUTALISK: [GLAVE_WURM_NORMAL],
    ZERG_GUARDIAN: [ACID_SPORE_NORMAL],
    ZERG_SCOURGE: [SUICIDE_SCOURGE],
    TORRARSQUE_ULTRALISK: [KAISER_BLADES_TORRASQUE],
    INFESTED_TERRAN: [SUICIDE_INFESTED_TERRAN],
    INFESTED_KERRIGAN: [CLAWS_INFESTED_KERRIGAN],
    HUNTER_KILLER_HYDRALISK: [NEEDLE_SPINES_HUNTER_KILLER],
    DEVOURING_ONE_ZERGLING: [CLAWS_DEVOURING_ONE],
    KUKULZA_MUTALISK: [GLAVE_WURM_KUKULZAMUTALISK],
    KUKULZA_GUARDIAN: [ACID_SPORE_KUKULZAGUARDIAN],
    TERRAN_VALKYRIE_FRIGATE: [HALO_ROCKETS],
    PROTOSS_CORSAIR: [NEUTRON_FLARE],
    PROTOSS_DARK_TEMPLAR_UNIT: [WARP_BLADES_NORMAL],
    ZERG_DEVOURER: [CORROSIVE_ACID],
    PROTOSS_PROBE: [PARTICLE_BEAM],
    PROTOSS_ZEALOT: [PSI_BLADES_NORMAL],
    PROTOSS_DRAGOON: [PHASE_DISRUPTOR_NORMAL],
    PROTOSS_ARCHON: [PSIONIC_SHOCKWAVE_NORMAL],
    PROTOSS_SCOUT: [DUAL_PHOTON_BLASTERS_NORMAL, ANTIMATTER_MISSILES_NORMAL],
    PROTOSS_ARBITER: [PHASE_DISRUPTOR_CANNON_NORMAL],
    PROTOSS_CARRIER: [PULSE_CANNON],
    PROTOSS_INTERCEPTOR: [PULSE_CANNON],
    DARK_TEMPLAR_HERO: [WARP_BLADES_DARK_TEMPLAR_HERO],
    ZERATUL_DARK_TEMPLAR: [WARP_BLADES_ZERATUL],
    TASSADAR_ZERATUL_ARCHON: [PSIONIC_SHOCKWAVE_TASSADAR_ZERATUL_ARCHON],
    FENIX_ZEALOT: [PSI_BLADES_FENIXZEALOT],
    TASSADAR_TEMPLAR: [PSI_ASSAULT_TASSADAR_ALDARIS],
    MOJO_SCOUT: [DUAL_PHOTON_BLASTERS_MOJO, ANITMATTER_MISSILES_MOJO],
    WARBRINGER_REAVER: [SCARAB],
    GANTRITHOR_CARRIER: [PULSE_CANNON],
    PROTOSS_REAVER: [SCARAB],
    DANIMOTH_ARBITER: [PHASE_DISRUPTOR_CANNON_DANIMOTH],
    ARTANIS_SCOUT: [DUAL_PHOTON_BLASTERS_ARTANIS, ANTIMATTER_MISSILES_ARTANIS],
    RASZAGAL: [NEUTRON_FLARE],
    SAMIR_DURAN_GHOST: [C10_CONCUSSION_RIFLE_SAMIR_DURAN],
    ALEXEI_STUKOV_GHOST: [C10_CONCUSSION_RIFLE_ALEXEI_STUKOV],
    GERARD_DUGALLE: [ATS_LASER_BATTERY_NORAD_II_MENGSK_DUGALLE, ATA_LASER_BATTERY_NORAD_II_MENGSK_DUGALLE],
    ZERG_LURKER: [SUBTERRANEAN_SPINES],
    INFESTED_DURAN: [C10_CONCUSSION_RIFLE_INFESTED_DURAN],
    TERRAN_MISSILE_TURRET: [LONGBOLT_MISSILES],
    ZERG_SPORE_COLONY: [SEEKER_SPORES],
    ZERG_SUNKEN_COLONY: [SUBTERRANEAN_TENTACLE],
    PROTOSS_PHOTON_CANNON: [STA_PHOTON_CANNON, STS_PHOTON_CANNON],
    FLOOR_MISSILE_TRAP: [HELLFIRE_MISSILE_PACK_FLOOR_TRAP],
    LEFT_WALL_MISSILE_TRAP: [HELLFIRE_MISSILE_PACK_WALL_TRAP],
    FLOOR_GUN_TRAP: [TWIN_AUTOCANNONS_FLOOR_TRAP],
    LEFT_WALL_FLAME_TRAP: [FLAME_THROWER_WALL_TRAP],
    RIGHT_WALL_MISSILE_TRAP: [HELLFIRE_MISSILE_PACK_WALL_TRAP],
    RIGHT_WALL_FLAME_TRAP: [FLAME_THROWER_WALL_TRAP]
}

if __name__ == '__main__':
    pass
