import dataclasses


def compare_dataclasses_ignoring_fields(obj1, obj2, *args) -> bool:
    """Compare two dataclasses and check if all fields are equal, ignoring those in
    *args."""
    assert type(obj1) is type(obj2)
    objs_are_equal = True
    for field in dataclasses.fields(obj1):
        if field not in args:
            objs_are_equal = getattr(obj1, field.name) == getattr(obj2, field.name)
    return objs_are_equal
