import dataclasses


@dataclasses.dataclass(frozen=True)
class ChkIoConfig:
    """Optional configuration for controlling how a StarCraft map is read and written.

    :param _use_strx: replace the 16 bit STR section with the 32 bit STRx. Use this if
        the map will have more than 65,535 strings.
    """

    _use_strx: bool = False

    @property
    def use_strx(self) -> bool:
        return self._use_strx
