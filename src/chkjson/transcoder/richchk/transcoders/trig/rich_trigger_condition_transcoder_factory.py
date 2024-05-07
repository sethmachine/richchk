""""""

from typing import Any, ClassVar, Optional, Type, Union

from .....model.richchk.trig.trigger_condition_id import TriggerConditionId
from .....util.subpackages_importer import import_all_modules_in_subpackage
from .rich_trigger_condition_transcoder import RichTriggerConditionTranscoder


class _RichTriggerConditionRegistrableTranscoder:
    def __init_subclass__(
        cls, trigger_condition_id: Optional[TriggerConditionId] = None
    ):
        RichTriggerConditionTranscoderFactory.register(trigger_condition_id, cls)


class RichTriggerConditionTranscoderFactory:
    transcoders: ClassVar[
        dict[
            TriggerConditionId,
            Type[
                Union[
                    RichTriggerConditionTranscoder[Any, Any],
                    _RichTriggerConditionRegistrableTranscoder,
                ]
            ],
        ]
    ] = {}

    @classmethod
    def make_rich_trig_action_transcoder(
        cls, condition_id: TriggerConditionId
    ) -> RichTriggerConditionTranscoder[Any, Any]:
        """Factory for making RichTrigActionTranscoder for a given trigger action ID."""
        try:
            maybe_transcoder: Union[
                RichTriggerConditionTranscoder[Any, Any],
                _RichTriggerConditionRegistrableTranscoder,
            ] = cls.transcoders[condition_id]()
            assert isinstance(maybe_transcoder, RichTriggerConditionTranscoder)
            retval: RichTriggerConditionTranscoder[Any, Any] = maybe_transcoder
            return retval
        except KeyError as err:
            raise NotImplementedError(f"{condition_id=} doesn't exist") from err

    @classmethod
    def register(
        cls,
        condition_id: Optional[TriggerConditionId],
        subclass: Type[_RichTriggerConditionRegistrableTranscoder],
    ) -> None:
        if condition_id is None:
            raise ValueError("Trigger condition ID must be defined")
        assert condition_id is not None
        actual_condition_id: TriggerConditionId = condition_id
        cls.transcoders[actual_condition_id] = subclass

    @classmethod
    def get_all_registered_condition_ids(cls) -> list[TriggerConditionId]:
        return [x for x in cls.transcoders.keys()]

    @classmethod
    def supports_transcoding_trig_action(cls, condition_id: TriggerConditionId) -> bool:
        return condition_id in cls.transcoders


# import all transcoder to register with the factory
# must happen after factory definition; otherwise causes circular import error
_THIS_MODULE_PARENT_PACKAGE_NAME = ".transcoder.richchk.transcoders.trig"
_TRANSCODERS_SUBPACKAGE_NAME = "conditions"

import_all_modules_in_subpackage(
    _THIS_MODULE_PARENT_PACKAGE_NAME, _TRANSCODERS_SUBPACKAGE_NAME
)
