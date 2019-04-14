"""

"""


import dataclasses
import io
import struct
import typing

from .abstract_chksection import _ChkSection, ChkSection
from .constants.unit_ids import *

NULL_CHAR = '\x00'

NUM_UNITS = 228
NUM_WEAPONS = 100


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


@dataclasses.dataclass(repr=False)
class _Base(_ChkSection, _Fields):
    pass


class ChkUnis(_Base, ChkSection):
    """Custom unit settings for the map.

    """
    name = 'UNIS'

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

    def to_json(self) -> dict:
        pass


if __name__ == '__main__':
    pass
