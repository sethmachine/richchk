""""""

from typing import Any, ClassVar, Optional, Type, Union

from .....model.richchk.trig.trigger_action_id import TriggerActionId
from .....util.subpackages_importer import import_all_modules_in_subpackage
from .rich_trigger_action_transcoder import RichTriggerActionTranscoder


class _RichTriggerActionRegistrableTranscoder:
    def __init_subclass__(cls, trigger_action_id: Optional[TriggerActionId] = None):
        RichTriggerActionTranscoderFactory.register(trigger_action_id, cls)


class RichTriggerActionTranscoderFactory:
    transcoders: ClassVar[
        dict[
            TriggerActionId,
            Type[
                Union[
                    RichTriggerActionTranscoder[Any, Any],
                    _RichTriggerActionRegistrableTranscoder,
                ]
            ],
        ]
    ] = {}

    @classmethod
    def make_rich_trigger_action_transcoder(
        cls, trig_action_id: TriggerActionId
    ) -> RichTriggerActionTranscoder[Any, Any]:
        """Factory for making RichTrigActionTranscoder for a given trigger action ID."""
        try:
            maybe_transcoder: Union[
                RichTriggerActionTranscoder[Any, Any],
                _RichTriggerActionRegistrableTranscoder,
            ] = cls.transcoders[trig_action_id]()
            assert isinstance(maybe_transcoder, RichTriggerActionTranscoder)
            retval: RichTriggerActionTranscoder[Any, Any] = maybe_transcoder
            return retval
        except KeyError as err:
            raise NotImplementedError(f"{trig_action_id=} doesn't exist") from err

    @classmethod
    def register(
        cls,
        trig_action_id: Optional[TriggerActionId],
        subclass: Type[_RichTriggerActionRegistrableTranscoder],
    ) -> None:
        if trig_action_id is None:
            raise ValueError("Trigger action ID must be defined")
        assert trig_action_id is not None
        actual_action_id: TriggerActionId = trig_action_id
        cls.transcoders[actual_action_id] = subclass

    @classmethod
    def get_all_registered_trig_action_ids(cls) -> list[TriggerActionId]:
        return [x for x in cls.transcoders.keys()]

    @classmethod
    def supports_transcoding_trig_action(cls, trig_action_id: TriggerActionId) -> bool:
        return trig_action_id in cls.transcoders


# import all transcoder to register with the factory
# must happen after factory definition; otherwise causes circular import error
_THIS_MODULE_PARENT_PACKAGE_NAME = ".transcoder.richchk.transcoders.trig"
_TRANSCODERS_SUBPACKAGE_NAME = "actions"

import_all_modules_in_subpackage(
    _THIS_MODULE_PARENT_PACKAGE_NAME, _TRANSCODERS_SUBPACKAGE_NAME
)
