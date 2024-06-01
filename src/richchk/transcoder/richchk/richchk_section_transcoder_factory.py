""""""

from typing import Any, ClassVar, Optional, Type, Union

from ...model.chk_section_name import ChkSectionName
from ...util.subpackages_importer import import_all_modules_in_subpackage
from .richchk_section_transcoder import RichChkSectionTranscoder


class _RichChkRegistrableTranscoder:
    def __init_subclass__(cls, chk_section_name: Optional[ChkSectionName] = None):
        RichChkSectionTranscoderFactory.register(chk_section_name, cls)


class RichChkSectionTranscoderFactory:
    transcoders: ClassVar[
        dict[
            ChkSectionName,
            Type[
                Union[RichChkSectionTranscoder[Any, Any], _RichChkRegistrableTranscoder]
            ],
        ]
    ] = {}

    @classmethod
    def make_chk_section_transcoder(
        cls, chk_section_name: ChkSectionName
    ) -> RichChkSectionTranscoder[Any, Any]:
        """Factory for making RichChkSectionTranscoder for a given CHK section name."""
        try:
            maybe_transcoder: Union[
                RichChkSectionTranscoder[Any, Any], _RichChkRegistrableTranscoder
            ] = cls.transcoders[chk_section_name]()
            assert isinstance(maybe_transcoder, RichChkSectionTranscoder)
            retval: RichChkSectionTranscoder[Any, Any] = maybe_transcoder
            return retval
        except KeyError as err:
            raise NotImplementedError(f"{chk_section_name=} doesn't exist") from err

    @classmethod
    def register(
        cls,
        chk_section_name: Optional[ChkSectionName],
        subclass: Type[_RichChkRegistrableTranscoder],
    ) -> None:
        if ChkSectionName is None:
            raise ValueError("ChkSectionName must be defined")
        assert chk_section_name is not None
        actual_chk_section_name: ChkSectionName = chk_section_name
        cls.transcoders[actual_chk_section_name] = subclass

    @classmethod
    def get_all_registered_chk_section_names(cls) -> list[ChkSectionName]:
        return [x for x in cls.transcoders.keys()]

    @classmethod
    def supports_transcoding_chk_section(cls, chk_section_name: ChkSectionName) -> bool:
        return chk_section_name in cls.transcoders


# import all transcoder to register with the factory
# must happen after factory definition; otherwise causes circular import error
_THIS_MODULE_PARENT_PACKAGE_NAME = ".transcoder.richchk"
_TRANSCODERS_SUBPACKAGE_NAME = "transcoders"

import_all_modules_in_subpackage(
    _THIS_MODULE_PARENT_PACKAGE_NAME, _TRANSCODERS_SUBPACKAGE_NAME
)
