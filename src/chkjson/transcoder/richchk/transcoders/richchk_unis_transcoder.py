"""Decode and encode the UNIS section which contains all unit settings.

Required for Vanilla and Hybrid (in Original mode). Not required for Melee. Validation:
Must be size of 4048 bytes. In Brood War scenarios, this section is replaced by "UNIx".

This section contains the unit settings for the level:

u8[228]: 1 byte for each unit, in order of Unit ID

00 - Unit does not use default settings 01 - Unit does use default settings

u32[228]: Hit points for unit (Note the displayed value is this value / 256, with the
low byte being a fractional HP value)

u16[228]: Shield points, in order of Unit ID

u8[228]: Armor points, in order of Unit ID

u16[228]: Build time (1/60 seconds), in order of Unit ID

u16[228]: Mineral cost, in order of Unit ID

u16[228]: Gas cost, in order of Unit ID

u16[228]: String number, in order of Unit ID

u16[100]: Base weapon damage the weapon does, in weapon ID order (#List of Unit Weapon
IDs)

u16[100]: Upgrade bonus weapon damage, in weapon ID order
"""


from ....model.chk.unis.decoded_unis_section import DecodedUnisSection
from ....model.richchk.unis.rich_unis_section import RichUnisSection
from ....transcoder.richchk.richchk_section_transcoder import RichChkSectionTranscoder
from ....transcoder.richchk.richchk_section_transcoder_factory import (
    _RichChkRegistrableTranscoder,
)


class RichChkUnisTranscoder(
    RichChkSectionTranscoder[RichUnisSection, DecodedUnisSection],
    _RichChkRegistrableTranscoder,
    chk_section_name=DecodedUnisSection.section_name(),
):
    def decode(self, decoded_chk_section: DecodedUnisSection) -> RichUnisSection:
        return RichUnisSection()

    def encode(self, rich_chk_section: RichUnisSection) -> DecodedUnisSection:
        return DecodedUnisSection([], [], [], [], [], [], [], [], [], [])
