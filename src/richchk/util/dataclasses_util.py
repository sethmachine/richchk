import dataclasses
from typing import TYPE_CHECKING, Any, Tuple, Type, TypeVar

if TYPE_CHECKING:
    from _typeshed import DataclassInstance

    _T = TypeVar("_T", bound=DataclassInstance)
else:
    _T = TypeVar("_T", bound=object)

_fields_by_type: dict[Type[Any], Tuple[Any, ...]] = {}


def build_dataclass_with_fields(from_obj: _T, **kwargs: Any) -> _T:
    """Build a new instance of the Dataclass, replacing fields with values in **kwargs.

    :param from_obj:
    :param kwargs:
    :return:
    """
    obj_type = type(from_obj)
    fields = _fields_by_type.get(obj_type)
    if fields is None:
        fields = dataclasses.fields(from_obj)
        _fields_by_type[obj_type] = fields
    new_fields = {}
    for field in fields:
        if not field.init:
            continue
        if field.name not in kwargs:
            new_fields[field.name] = getattr(from_obj, field.name)
        else:
            new_fields[field.name] = kwargs[field.name]
    return obj_type(**new_fields)
