from test.chk_resources import DEMON_LORE_YATAPI_TEST_CHK_FILE_PATH, SCX_CHK_FILE
from test.io.richchk.rich_chk_io_test import assert_chks_are_equal

from richchk.io.chk.chk_io import ChkIo
from richchk.io.richchk.richchk_io import RichChkIo
from richchk.model.chk.decoded_chk import DecodedChk


def _decode(path: str) -> tuple[DecodedChk, object]:
    chk = ChkIo().decode_chk_file(path)
    return chk, RichChkIo().decode_chk(chk)


def test_encoding_the_same_rich_chk_twice_builds_a_new_result_each_time():
    chk, rich_chk = _decode(SCX_CHK_FILE)
    io = RichChkIo()
    first = io.encode_chk(rich_chk)
    second = io.encode_chk(rich_chk)
    assert first is not second
    assert_chks_are_equal(first, chk)
    assert_chks_are_equal(second, chk)


def test_encoding_maps_alternately_in_one_process_matches_encoding_each_alone():
    _, rich_a = _decode(SCX_CHK_FILE)
    _, rich_b = _decode(DEMON_LORE_YATAPI_TEST_CHK_FILE_PATH)
    expected_a = RichChkIo().encode_chk(rich_a)
    expected_b = RichChkIo().encode_chk(rich_b)
    io = RichChkIo()
    for _ in range(2):
        assert_chks_are_equal(io.encode_chk(rich_a), expected_a)
        assert_chks_are_equal(io.encode_chk(rich_b), expected_b)


def test_a_new_io_object_gives_the_same_result_as_a_reused_one():
    chk, rich_chk = _decode(SCX_CHK_FILE)
    reused = RichChkIo()
    reused.encode_chk(rich_chk)
    assert_chks_are_equal(reused.encode_chk(rich_chk), RichChkIo().encode_chk(rich_chk))
