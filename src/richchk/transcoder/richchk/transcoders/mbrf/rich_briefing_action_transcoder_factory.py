""""""

from typing import Any, ClassVar, Optional, Type, Union

from .....model.richchk.mbrf.briefing_action_id import BriefingActionId
from .....util.subpackages_importer import import_all_modules_in_subpackage
from .rich_briefing_action_transcoder import RichBriefingActionTranscoder


class _RichBriefingActionRegistrableTranscoder:
    def __init_subclass__(
        cls, briefing_action_id: Optional[BriefingActionId] = None
    ) -> None:
        RichBriefingActionTranscoderFactory.register(briefing_action_id, cls)


class RichBriefingActionTranscoderFactory:
    transcoders: ClassVar[
        dict[
            BriefingActionId,
            Type[
                Union[
                    RichBriefingActionTranscoder[Any, Any],
                    _RichBriefingActionRegistrableTranscoder,
                ]
            ],
        ]
    ] = {}
    _instances: ClassVar[
        dict[BriefingActionId, RichBriefingActionTranscoder[Any, Any]]
    ] = {}

    @classmethod
    def make_rich_briefing_action_transcoder(
        cls, briefing_action_id: BriefingActionId
    ) -> RichBriefingActionTranscoder[Any, Any]:
        cached = cls._instances.get(briefing_action_id)
        if cached is not None:
            return cached
        try:
            maybe_transcoder: Union[
                RichBriefingActionTranscoder[Any, Any],
                _RichBriefingActionRegistrableTranscoder,
            ] = cls.transcoders[briefing_action_id]()
            assert isinstance(maybe_transcoder, RichBriefingActionTranscoder)
            retval: RichBriefingActionTranscoder[Any, Any] = maybe_transcoder
            cls._instances[briefing_action_id] = retval
            return retval
        except KeyError as err:
            raise NotImplementedError(f"{briefing_action_id=} doesn't exist") from err

    @classmethod
    def register(
        cls,
        briefing_action_id: Optional[BriefingActionId],
        subclass: Type[_RichBriefingActionRegistrableTranscoder],
    ) -> None:
        if briefing_action_id is None:
            raise ValueError("Briefing action ID must be defined")
        cls.transcoders[briefing_action_id] = subclass

    @classmethod
    def supports_transcoding_briefing_action(
        cls, briefing_action_id: BriefingActionId
    ) -> bool:
        return briefing_action_id in cls.transcoders


# import all transcoders to register with the factory
_THIS_MODULE_PARENT_PACKAGE_NAME = ".transcoder.richchk.transcoders.mbrf"
_TRANSCODERS_SUBPACKAGE_NAME = "actions"

import_all_modules_in_subpackage(
    _THIS_MODULE_PARENT_PACKAGE_NAME, _TRANSCODERS_SUBPACKAGE_NAME
)
