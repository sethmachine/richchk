import pytest

from richchk.model.mpq.stormlib.wav.stormlib_wav import StormLibWav
from richchk.model.richchk.mrgn.rich_mrgn_lookup import RichMrgnLookup
from richchk.model.richchk.richchk_encode_context import RichChkEncodeContext
from richchk.model.richchk.str.rich_str_lookup import RichStrLookup
from richchk.model.richchk.swnm.rich_swnm_lookup import RichSwnmLookup
from richchk.model.richchk.trig.actions.play_wav_action import PlayWavAction
from richchk.model.richchk.uprp.rich_cuwp_lookup import RichCuwpLookup
from richchk.model.richchk.wav.rich_wav_lookup import RichWavMetadataLookup
from richchk.transcoder.richchk.transcoders.trig.actions.play_wav_action_transcoder import (
    RichTriggerPlayWavActionTranscoder,
)
from richchk.util.dataclasses_util import build_dataclass_with_fields


@pytest.fixture(scope="function")
def play_wav_action():
    return PlayWavAction(_path_to_wav_in_mpq="wav.wav", _duration_ms=None)


@pytest.fixture(scope="function")
def play_wav_action_with_no_metadata():
    return PlayWavAction(_path_to_wav_in_mpq="wav-no-metadata.wav", _duration_ms=None)


@pytest.fixture(scope="function")
def play_wav_metadata(play_wav_action):
    return StormLibWav(
        _path_to_wav_in_mpq=play_wav_action.path_to_wav_in_mpq,
        _duration_ms=1000,
    )


@pytest.fixture(scope="function")
def rich_chk_encode_context(play_wav_action, play_wav_action_with_no_metadata):
    return RichChkEncodeContext(
        _rich_str_lookup=RichStrLookup(
            _string_by_id_lookup={},
            _id_by_string_lookup={
                play_wav_action.path_to_wav_in_mpq: 0,
                play_wav_action_with_no_metadata.path_to_wav_in_mpq: 1,
            },
        ),
        _rich_mrgn_lookup=RichMrgnLookup(
            _location_by_id_lookup={}, _id_by_location_lookup={}
        ),
        _rich_swnm_lookup=RichSwnmLookup(
            _switch_by_id_lookup={}, _id_by_switch_lookup={}
        ),
        _rich_cuwp_lookup=RichCuwpLookup(_cuwp_by_id_lookup={}, _id_by_cuwp_lookup={}),
        _wav_metadata_lookup=RichWavMetadataLookup(
            _metadata_by_wav_path={
                play_wav_action.path_to_wav_in_mpq: StormLibWav(
                    _path_to_wav_in_mpq=play_wav_action.path_to_wav_in_mpq,
                    _duration_ms=1000,
                )
            }
        ),
    )


def test_it_encodes_action_if_duration_unspecified_and_in_metadata(
    play_wav_action, play_wav_metadata, rich_chk_encode_context
):
    decoded_action = RichTriggerPlayWavActionTranscoder().encode(
        play_wav_action, rich_chk_encode_context
    )
    assert decoded_action.time == play_wav_metadata.duration_ms


def test_it_encodes_action_with_overriden_duration_if_specified(
    play_wav_action, play_wav_metadata, rich_chk_encode_context
):
    expected_duration_not_in_metadata = play_wav_metadata.duration_ms * 2
    transcoder = RichTriggerPlayWavActionTranscoder()
    decoded_action = transcoder.encode(
        build_dataclass_with_fields(
            play_wav_action, _duration_ms=expected_duration_not_in_metadata
        ),
        rich_chk_encode_context,
    )
    assert decoded_action.time == expected_duration_not_in_metadata


def test_it_encodes_with_duration_specified_if_no_metadata(
    play_wav_action_with_no_metadata, rich_chk_encode_context
):
    expected_duration = 1000
    decoded_action = RichTriggerPlayWavActionTranscoder().encode(
        build_dataclass_with_fields(
            play_wav_action_with_no_metadata, _duration_ms=expected_duration
        ),
        rich_chk_encode_context,
    )
    assert decoded_action.time == expected_duration


def test_it_throws_if_encoding_and_no_duration_specified_and_not_in_metadata(
    play_wav_action_with_no_metadata, rich_chk_encode_context
):
    with pytest.raises(ValueError):
        RichTriggerPlayWavActionTranscoder().encode(
            play_wav_action_with_no_metadata, rich_chk_encode_context
        )


def test_it_throws_if_encoding_unspecified_duration_and_no_metadata_exists(
    play_wav_action, rich_chk_encode_context
):
    with pytest.raises(ValueError):
        RichTriggerPlayWavActionTranscoder().encode(
            play_wav_action,
            build_dataclass_with_fields(
                rich_chk_encode_context,
                _wav_metadata_lookup=RichWavMetadataLookup(_metadata_by_wav_path={}),
            ),
        )
