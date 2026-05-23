"""Force property flags as used in the FORC section.

See:
http://staredit.net/wiki/index.php/Scenario.chk#.22FORC.22_-_Force_Settings

Bit 0 - Random start location
Bit 1 - Allies
Bit 2 - Allied victory
Bit 3 - Shared vision
"""

import dataclasses


@dataclasses.dataclass(frozen=True)
class ForceFlags:
    """Property flags for a single force.

    :param _random_start: bit 0 - players on this force start at random locations
    :param _allies: bit 1 - players on this force are allied
    :param _allied_victory: bit 2 - players on this force share victory condition
    :param _shared_vision: bit 3 - players on this force share vision
    """

    _random_start: bool = False
    _allies: bool = False
    _allied_victory: bool = False
    _shared_vision: bool = False

    @property
    def random_start(self) -> bool:
        return self._random_start

    @property
    def allies(self) -> bool:
        return self._allies

    @property
    def allied_victory(self) -> bool:
        return self._allied_victory

    @property
    def shared_vision(self) -> bool:
        return self._shared_vision
