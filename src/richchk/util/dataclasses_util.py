import dataclasses
from typing import TYPE_CHECKING, Any, TypeVar

if TYPE_CHECKING:
    from _typeshed import DataclassInstance

    _T = TypeVar("_T", bound=DataclassInstance)
else:
    _T = TypeVar("_T", bound=object)


def build_dataclass_with_fields(from_obj: _T, **kwargs: Any) -> _T:
    """Build a new instance of the Dataclass, replacing fields with values in **kwargs.

    :param from_obj:
    :param kwargs:
    :return:
    """
    new_fields = {}
    for field in dataclasses.fields(from_obj):
        if field.name not in kwargs:
            new_fields[field.name] = getattr(from_obj, field.name)
        else:
            new_fields[field.name] = kwargs[field.name]
    return type(from_obj)(**new_fields)
