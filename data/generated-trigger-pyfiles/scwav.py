"""Wrapper for a Starcraft Wav reference.

"""


class SCWav:
    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return self.value


SOUNDPROTOSSARBITERPABFOL01WAV = SCWav('"sound\\Protoss\\ARBITER\\PAbFol01.WAV"')
SOUNDPROTOSSARBITERPABFOL02WAV = SCWav('"sound\\Protoss\\ARBITER\\PAbFol02.WAV"')
SOUNDPROTOSSWITNESSPWIPSS00WAV = SCWav('"sound\\Protoss\\Witness\\PWiPss00.WAV"')
SOUNDTERRANMEDICTMEDRESTWAV = SCWav('"sound\\Terran\\Medic\\TMedRest.wav"')
SOUNDZERGULTRAZULPSS02WAV = SCWav('"sound\\Zerg\\Ultra\\ZUlPss02.WAV"')
SOUNDZERGZERGDURANZDNPSS01WAV = SCWav('"sound\\Zerg\\ZergDuran\\ZDnPss01.wav"')
STAREDITWAV28_DRAGON_QUEST_MONSTERS_2__ITEM_DISCOVEREDWAV = SCWav('"staredit\\wav\\28 Dragon Quest Monsters 2 - Item Discovered.wav"')
STAREDITWAVP8B02RASWAV = SCWav('"staredit\\wav\\P8B02RAS.wav"')
STAREDITWAVZ5M30FEDWAV = SCWav('"staredit\\wav\\Z5M30FED.wav"')
STAREDITWAVCHANT1WAV = SCWav('"staredit\\wav\\chant1.wav"')
