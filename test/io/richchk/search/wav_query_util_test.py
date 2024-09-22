from test.chk_resources import SCX_CHK_FILE

import pytest

from richchk.io.chk.chk_io import ChkIo
from richchk.io.richchk.query.wav_query_util import WavQueryUtil
from richchk.io.richchk.richchk_io import RichChkIo
from richchk.model.richchk.rich_chk import RichChk
from richchk.model.richchk.str.rich_string import RichString
from richchk.model.richchk.wav.rich_wav import RichWav
from richchk.model.richchk.wav.rich_wav_section import RichWavSection


@pytest.fixture(scope="function")
def rich_chk_with_wavs():
    return RichChk(
        _chk_sections=[
            RichWavSection(
                _wavs=[
                    RichWav(
                        _path_in_chk=RichString(_value="staredit\\wav\\hello.wav"),
                        _index=0,
                    ),
                    RichWav(
                        _path_in_chk=RichString(_value="staredit\\wav\\world.wav"),
                        _index=1,
                    ),
                ]
            )
        ]
    )


@pytest.fixture(scope="function")
def real_rich_chk_with_wav():
    # contains 3 WAV entries already
    # 0 = {RichWav}
    # RichWav(_path_in_chk=RichString(_value='staredit\\wav\\monitor humming.1.wav'), _index=0)
    # 1 = {RichWav}
    # RichWav(_path_in_chk=RichString(_value='staredit\\wav\\monitor humming.2.wav'), _index=1)
    # 2 = {RichWav}
    # RichWav(_path_in_chk=RichString(_value='staredit\\wav\\monitor humming.3.wav'), _index=2)
    return RichChkIo().decode_chk(ChkIo().decode_chk_file(SCX_CHK_FILE))


def test_it_finds_only_wav_by_basename(rich_chk_with_wavs):
    bn1 = "hello.wav"
    bn2 = "world.wav"
    wav1 = WavQueryUtil.find_only_wav_by_basename(bn1, rich_chk_with_wavs)
    assert bn1 in wav1.path_in_chk.value
    assert bn2 not in wav1.path_in_chk.value
    wav2 = WavQueryUtil.find_only_wav_by_basename(bn2, rich_chk_with_wavs)
    assert bn2 in wav2.path_in_chk.value
    assert bn1 not in wav2.path_in_chk.value


def test_it_throws_if_no_basename_found(rich_chk_with_wavs):
    bn_with_no_wav = "foobar.wav"
    with pytest.raises(ValueError):
        WavQueryUtil.find_only_wav_by_basename(bn_with_no_wav, rich_chk_with_wavs)


def test_it_finds_only_wav_by_exact_match(rich_chk_with_wavs):
    search1 = "staredit\\wav\\hello.wav"
    search2 = "staredit\\wav\\world.wav"
    wav1 = WavQueryUtil.find_only_wav_by_exact_match(search1, rich_chk_with_wavs)
    assert search1 == wav1.path_in_chk.value
    wav2 = WavQueryUtil.find_only_wav_by_exact_match(search2, rich_chk_with_wavs)
    assert search2 == wav2.path_in_chk.value


def test_it_throws_if_no_exact_match_found(rich_chk_with_wavs):
    search = "staredit\\wav\\worlds.wav"
    with pytest.raises(ValueError):
        WavQueryUtil.find_only_wav_by_exact_match(search, rich_chk_with_wavs)


def test_integration_it_finds_only_wav_by_basename(real_rich_chk_with_wav):
    expected_basenames = [
        "monitor humming.1.wav",
        "monitor humming.2.wav",
        "monitor humming.3.wav",
    ]
    for bn in expected_basenames:
        found_wav = WavQueryUtil.find_only_wav_by_basename(bn, real_rich_chk_with_wav)
        assert bn in found_wav.path_in_chk.value


def test_integration_it_finds_by_exact_match(real_rich_chk_with_wav):
    search = "staredit\\wav\\monitor humming.1.wav"
    found_wav = WavQueryUtil.find_only_wav_by_exact_match(
        search, real_rich_chk_with_wav
    )
    assert search == found_wav.path_in_chk.value
