"""Verify equality works as expected given we have custom overrides for __eq__ and
__hash__"""

from richchk.model.richchk.str.rich_string import RichString
from richchk.model.richchk.swnm.rich_switch import RichSwitch


def test_switches_are_not_equal_if_all_fields_undefined():
    switch1 = RichSwitch()
    switch2 = RichSwitch()
    assert switch1 != switch2


def test_switches_are_unique_in_set_if_all_fields_undefined():
    switch1 = RichSwitch()
    switch2 = RichSwitch()
    _assert_switches_are_unique_in_set([switch1, switch2])


def test_switches_are_not_equal_if_different_name_and_no_index():
    switch1 = RichSwitch(_custom_name=RichString(_value="foo"), _index=None)
    switch2 = RichSwitch(_custom_name=RichString(_value="bar"), _index=None)
    assert switch1 != switch2


def test_switches_are_unique_in_set_if_different_name_and_no_index():
    switch1 = RichSwitch(_custom_name=RichString(_value="foo"), _index=None)
    switch2 = RichSwitch(_custom_name=RichString(_value="bar"), _index=None)
    _assert_switches_are_unique_in_set([switch1, switch2])


def test_switches_are_equal_if_same_name_but_undefined_index():
    switch1 = RichSwitch(_custom_name=RichString(_value="foo"), _index=None)
    switch2 = RichSwitch(_custom_name=RichString(_value="foo"), _index=None)
    assert switch1 == switch2


def test_switches_are_same_in_set_if_same_name_but_undefined_index():
    switch1 = RichSwitch(_custom_name=RichString(_value="foo"), _index=None)
    switch2 = RichSwitch(_custom_name=RichString(_value="foo"), _index=None)
    _assert_switches_are_same_in_set([switch1, switch2])


def test_switches_are_different_if_same_name_and_different_index():
    switch1 = RichSwitch(_custom_name=RichString(_value="foo"), _index=0)
    switch2 = RichSwitch(_custom_name=RichString(_value="foo"), _index=1)
    assert switch1 != switch2


def test_switches_are_equal_if_different_name_but_same_index():
    switch1 = RichSwitch(_custom_name=RichString(_value="foo"), _index=0)
    switch2 = RichSwitch(_custom_name=RichString(_value="bar"), _index=0)
    assert switch1 == switch2


def _assert_switches_are_unique_in_set(switches):
    switch_set = set(switches)
    assert len(switch_set) == len(switches)
    assert all([s in switch_set for s in switches])


def _assert_switches_are_same_in_set(switches):
    switch_set = set(switches)
    assert len(switch_set) == 1
    assert all([s in switch_set for s in switches])
