from richchk.model.chk.wav.decoded_wav_section import DecodedWavSection
from richchk.transcoder.chk.transcoders.chk_wav_transcoder import ChkWavTranscoder

from ....chk_resources import CHK_SECTION_FILE_PATHS


def _read_chk_section() -> bytes:
    with open(
        CHK_SECTION_FILE_PATHS[DecodedWavSection.section_name().value], "rb"
    ) as f:
        chk_binary_data = f.read()
    return chk_binary_data


def test_it_decodes_expected_wav_string_ids():
    transcoder = ChkWavTranscoder()
    chk_binary_data = _read_chk_section()
    wav = transcoder.decode(chk_binary_data)
    assert len(wav.wav_string_ids) == ChkWavTranscoder.NUM_WAVS
    # theres a single WAV file used in the CHK right now
    assert wav.wav_string_ids[0] != 0
    assert all(x == 0 for x in wav.wav_string_ids[1:])


def test_it_decodes_and_encodes_without_changing_data():
    transcoder = ChkWavTranscoder()
    chk_binary_data = _read_chk_section()
    wav = transcoder.decode(chk_binary_data)
    actual_encoded_data = transcoder.encode(wav, include_header=False)
    assert actual_encoded_data == chk_binary_data
    assert transcoder.decode(actual_encoded_data) == transcoder.decode(chk_binary_data)
