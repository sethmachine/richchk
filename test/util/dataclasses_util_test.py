""""""

import dataclasses

from chkjson.util.dataclasses_util import build_dataclass_with_fields


@dataclasses.dataclass
class TestDataclass:
    field1: int
    field2: bool
    field3: bool = False


def test_it_creates_new_dataclass_with_fields_provided():
    obj1 = TestDataclass(0, True, True)
    new_obj = build_dataclass_with_fields(obj1, field2=False, field3=True)
    expected_obj = TestDataclass(0, False, True)
    assert obj1 != new_obj
    assert new_obj == expected_obj


def test_it_creates_same_object_if_no_fields_provided():
    obj1 = TestDataclass(1, False, False)
    new_obj = build_dataclass_with_fields(obj1)
    assert new_obj == obj1
    assert id(new_obj) != id(obj1)


def test_it_ignores_unknown_fields():
    obj1 = TestDataclass(1, False, False)
    new_obj = build_dataclass_with_fields(obj1, not_a_field=1234)
    assert new_obj == obj1
    assert id(new_obj) != id(obj1)
