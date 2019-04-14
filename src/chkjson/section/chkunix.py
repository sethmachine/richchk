"""

"""


import dataclasses
import io
import struct
import typing

from .abstract_chksection import _ChkSection, ChkSection
from .constants.unit_ids import *
from .constants.unit_to_weapon_ids import UNIT_TO_WEAPON, PRIMARY, SECONDARY
from . import chkstr

NULL_CHAR = '\x00'

NUM_UNITS = 228
NUM_WEAPONS = 130


@dataclasses.dataclass
class UnitSetting:
    """Represents a custom unit setting for its name, health, etc.

    unit_id: the unit ID, must be a number between 0-228
    hitpoints: the health of the unit (multiplied by 256 in UNIx)
    shields: the shields of the unit
    armor: the armor of the unit
    build_time: the build time of the unit in seconds (multiplied by 60 in UNIx)
    minerals: cost in minerals to build/repair the unit
    gas: cost in gas to build/repair the unit
    weapons: a list of weapon IDs that the unit uses, usually one element
    weapon_damage: base damage for each weapon of the unit;
                   the first element is the primary weapon, the 2nd is the secondary weapon (if any)
                   secondary weapons are almost always for attacks against air units
    weapon_bonus: upgrade bonus for each weapon of the unit
    name: a custom name for the unit (will be added to the STR if the string does not exist)

    """
    unit_id: int
    hitpoints: int = None
    shields: int = None
    armor: int = None
    build_time: int = None
    minerals: int = None
    gas: int = None
    weapon_damage: typing.List[int] = None
    weapon_bonus: typing.List[int] = None
    name: str = None
    weapons: typing.List[int] = None

    def __post_init__(self):
        self.weapons = UNIT_TO_WEAPON.get(self.unit_id)


@dataclasses.dataclass(repr=False)
class _Fields:
    """Custom unit settings for the map.

    This section contains the unit settings for the level:

    u8[228]: 1 byte for each unit, in order of Unit ID
    00 - Unit does not use default settings
    01 - Unit does use default settings
    u32[228]: Hit points for unit (Note the displayed value is this value / 256, with the low byte being a fractional HP value)
    u16[228]: Shield points, in order of Unit ID
    u8[228]: Armor points, in order of Unit ID
    u16[228]: Build time (1/60 seconds), in order of Unit ID
    u16[228]: Mineral cost, in order of Unit ID
    u16[228]: Gas cost, in order of Unit ID
    u16[228]: String number, in order of Unit ID
    u16[228]: Base weapon damage the weapon does, in weapon ID order (#List of Unit Weapon IDs)
    u16[228]: Upgrade bonus weapon damage, in weapon ID order

    """
    use_settings_flags: typing.List[int]
    hitpoints: typing.List[int]
    shields: typing.List[int]
    armor: typing.List[int]
    build_time: typing.List[int]
    minerals: typing.List[int]
    gas: typing.List[int]
    string_ids: typing.List[int]
    weapon_damage: typing.List[int]
    weapon_bonus: typing.List[int]
    str_: chkstr.ChkStr = None


@dataclasses.dataclass(repr=False)
class _Base(_ChkSection, _Fields):
    pass

class ChkUnix(_Base, ChkSection):
    """Custom unit settings for the map.

    """
    name = 'UNIx'

    def __post_init__(self):
        for cls in self.__class__.__bases__:
            super(self.__class__, self).__post_init__()

    @classmethod
    def _decompile(cls, data: io.BytesIO) -> ChkSection:
        use_settings_flags = [struct.unpack('B', data.read(1))[0] for unit in range(NUM_UNITS)]
        hitpoints = [struct.unpack('I', data.read(4))[0] for unit in range(NUM_UNITS)]
        shields = [struct.unpack('H', data.read(2))[0] for unit in range(NUM_UNITS)]
        armor = [struct.unpack('B', data.read(1))[0] for unit in range(NUM_UNITS)]
        build_time = [struct.unpack('H', data.read(2))[0] for unit in range(NUM_UNITS)]
        minerals = [struct.unpack('H', data.read(2))[0] for unit in range(NUM_UNITS)]
        gas = [struct.unpack('H', data.read(2))[0] for unit in range(NUM_UNITS)]
        string_ids = [struct.unpack('H', data.read(2))[0] for unit in range(NUM_UNITS)]
        weapon_damage = [struct.unpack('H', data.read(2))[0] for unit in range(NUM_WEAPONS)]
        weapon_bonus = [struct.unpack('H', data.read(2))[0] for unit in range(NUM_WEAPONS)]
        return cls(use_settings_flags=use_settings_flags, hitpoints=hitpoints, shields=shields, armor=armor,
                   build_time=build_time, minerals=minerals, gas=gas, string_ids=string_ids,
                   weapon_damage=weapon_damage, weapon_bonus=weapon_bonus)

    def compile(self, header=True) -> bytes:
        """

        :return:
        """
        data = b''
        data += struct.pack('{}B'.format(len(self.use_settings_flags)), *self.use_settings_flags)
        data += struct.pack('{}I'.format(len(self.hitpoints)), *self.hitpoints)
        data += struct.pack('{}H'.format(len(self.shields)), *self.shields)
        data += struct.pack('{}B'.format(len(self.armor)), *self.armor)
        data += struct.pack('{}H'.format(len(self.build_time)), *self.build_time)
        data += struct.pack('{}H'.format(len(self.minerals)), *self.minerals)
        data += struct.pack('{}H'.format(len(self.gas)), *self.gas)
        data += struct.pack('{}H'.format(len(self.string_ids)), *self.string_ids)
        data += struct.pack('{}H'.format(len(self.weapon_damage)), *self.weapon_damage)
        data += struct.pack('{}H'.format(len(self.weapon_bonus)), *self.weapon_bonus)
        if header:
            header_ = self._compile_header(self.__class__.name, len(data))
            data = header_ + data
        return data

    def add_unit_setting(self, setting: UnitSetting):
        """Modifies a unit setting, updating the data structures and STR section appropriately.

        :param setting: a modification to a unit (name, shields, armor, etc.)
        :return:
        """
        index = setting.unit_id
        self.use_settings_flags[index] = 0
        if setting.hitpoints is not None:
            self.hitpoints[index] = setting.hitpoints * 256
        if setting.shields is not None:
            self.shields[index] = setting.shields
        if setting.armor is not None:
            self.armor[index] = setting.armor
        if setting.build_time is not None:
            self.build_time[index] = setting.build_time
        if setting.minerals is not None:
            self.minerals[index] = setting.minerals
        if setting.gas is not None:
            self.gas[index] = setting.gas
        if setting.weapons is not None:
            if setting.weapon_damage is not None:
                for i, damage in enumerate(setting.weapon_damage):
                    weapon = setting.weapons[i]
                    self.weapon_damage[weapon] = damage
            if setting.weapon_bonus is not None:
                for i, bonus in enumerate(setting.weapon_bonus):
                    weapon = setting.weapons[i]
                    self.weapon_bonus[weapon] = bonus
        # add string to table if it doesn't exist...
        if setting.name is not None:
            if not self.str_.exists(setting.name):
                self.str_.add_string(setting.name)
            string_index = self.str_.get_index(setting.name)
            self.string_ids[index] = string_index + 1

    def to_json(self) -> dict:
        data = vars(self)
        return {key: data[key] for key in data if type(data[key]) == list}


if __name__ == '__main__':
    pass
