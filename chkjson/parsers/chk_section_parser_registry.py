# type: ignore
# seems to be a bug with mypy: https://github.com/python/mypy/issues/11619
"""Register all CHK section parsers.

I tried following https://charlesreid1.github.io/python-patterns-the-registry.html
but it doesn't seem to work.  I think reflection is needed to force Python to load
all the candidate subclasses so they are registered properly.
E.g. see: https://towardsdatascience.com/python-polymorphism-with-class-discovery-28908ac6456f

But that seems pretty hacky, so I'm just going to manually register each parser here.

"""


from typing import TypeVar

from chkjson.model.chk.chk_section_names import ChkSectionName
from chkjson.parsers.sections.abstract_chk_section_parser import (
    AbstractChkSectionParser,
)
from chkjson.parsers.sections.chk_str_parser import ChkStrParser

T = TypeVar("T", bound=AbstractChkSectionParser)


class ChkSectionParserRegistry:
    _REGISTRY: dict[ChkSectionName, AbstractChkSectionParser] = {
        ChkStrParser.chk_section_name.fget(ChkStrParser): ChkStrParser
    }

    @classmethod
    def get_registry(cls):
        return dict(cls._REGISTRY)

    @classmethod
    def get_by_chk_section_name(cls, chk_section_name: ChkSectionName):
        return cls._REGISTRY[chk_section_name]

    @classmethod
    def contains(cls, chk_section_name: ChkSectionName):
        return chk_section_name in cls._REGISTRY
