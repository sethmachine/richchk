"""Represents a single force (team) in the FORC section."""

import dataclasses

from ..str.rich_string import RichNullString, RichString
from .force_flags import ForceFlags


@dataclasses.dataclass(frozen=True)
class RichForce:
    """A single StarCraft force (team) with a name and property flags.

    :param _name: display name of this force; RichNullString means use the default name
    :param _flags: property flags controlling alliance, vision sharing, etc.
    """

    _name: RichString = dataclasses.field(default_factory=RichNullString)
    _flags: ForceFlags = dataclasses.field(default_factory=ForceFlags)

    @property
    def name(self) -> RichString:
        return self._name

    @property
    def flags(self) -> ForceFlags:
        return self._flags
