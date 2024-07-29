""""""


import pytest

from richchk.editor.richchk.rich_wav_editor import RichWavEditor
from richchk.model.chk.wav.wav_constants import MAX_WAV_FILES
from richchk.model.richchk.str.rich_string import RichString
from richchk.model.richchk.wav.rich_wav import RichWav
from richchk.model.richchk.wav.rich_wav_section import RichWavSection


@pytest.fixture(scope="function")
def rich_wav():
    return RichWavSection(
        _wavs=[RichWav(_path_in_chk=RichString(_value="wavfile.wav"), _index=0)]
    )


def test_integration_it_adds_wavs_to_wav_and_allocates_index_to_each(rich_wav):
    editor = RichWavEditor()
    wavs_to_add = ["wav1.wav", "wav2.wav"]
    expected_wavs = rich_wav.wavs + [
        RichWav(_path_in_chk=RichString(_value=wavs_to_add[0]), _index=1),
        RichWav(_path_in_chk=RichString(_value=wavs_to_add[1]), _index=2),
    ]
    new_wav = editor.add_wav_files(wavs_to_add, rich_wav)
    assert len(new_wav.wavs) == 3
    for expected in expected_wavs:
        assert expected in new_wav.wavs


def test_integration_it_does_not_add_duplicate_wavs(rich_wav):
    editor = RichWavEditor()
    wavs_to_add = [rich_wav.wavs[0].path_in_chk.value]
    new_wav = editor.add_wav_files(wavs_to_add, rich_wav)
    assert len(new_wav.wavs) == 1
    assert new_wav.wavs == rich_wav.wavs


def test_integration_it_allocates_all_possible_ids(rich_wav):
    editor = RichWavEditor()
    # there's a 1 WAV already inside the rich wav, so we can add MAX_WAV_FILES - 1 more
    wavs_to_add = [f"{x}.wav" for x in range(1, MAX_WAV_FILES)]
    new_wav = editor.add_wav_files(wavs_to_add, rich_wav)
    assert len(new_wav.wavs) == MAX_WAV_FILES


def test_it_throws_if_allocating_more_ids_than_max(rich_wav):
    editor = RichWavEditor()
    # there's a 1 WAV already inside the rich wav, so we can add MAX_WAV_FILES - 1 more
    wavs_to_add = [f"{x}.wav" for x in range(1, MAX_WAV_FILES + 1)]
    with pytest.raises(ValueError):
        editor.add_wav_files(wavs_to_add, rich_wav)
