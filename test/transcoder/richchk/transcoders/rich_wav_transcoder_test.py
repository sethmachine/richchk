import pytest

from richchk.model.chk.wav.decoded_wav_section import DecodedWavSection
from richchk.model.chk.wav.wav_constants import MAX_WAV_FILES, UNUSED_WAV_STRING_ID
from richchk.model.richchk.mrgn.rich_mrgn_lookup import RichMrgnLookup
from richchk.model.richchk.richchk_decode_context import RichChkDecodeContext
from richchk.model.richchk.richchk_encode_context import RichChkEncodeContext
from richchk.model.richchk.str.rich_str_lookup import RichStrLookup
from richchk.model.richchk.str.rich_string import RichString
from richchk.model.richchk.swnm.rich_swnm_lookup import RichSwnmLookup
from richchk.model.richchk.uprp.rich_cuwp_lookup import RichCuwpLookup
from richchk.model.richchk.wav.rich_wav import RichWav
from richchk.model.richchk.wav.rich_wav_section import RichWavSection
from richchk.transcoder.chk.transcoders.chk_wav_transcoder import ChkWavTranscoder
from richchk.transcoder.richchk.transcoders.rich_wav_transcoder import (
    RichChkWavTranscoder,
)

from ....chk_resources import CHK_SECTION_FILE_PATHS

# the only WAV entry in test-chk-transcoder-inputs (from test-chkjson-scx.chk)
_EXPECTED_RICH_WAV = RichWav(
    _path_in_chk=RichString(_value="staredit\\wav\\monitor humming.1.wav"), _index=0
)


@pytest.fixture
def real_decoded_wav() -> DecodedWavSection:
    with open(
        CHK_SECTION_FILE_PATHS[DecodedWavSection.section_name().value], "rb"
    ) as f:
        chk_binary_data = f.read()
    return ChkWavTranscoder().decode(chk_binary_data)


@pytest.fixture
def real_rich_chk_decode_context(real_decoded_wav) -> RichChkDecodeContext:
    # the lookups are based on the real WAV filepaths in the CHK
    return RichChkDecodeContext(
        _rich_str_lookup=RichStrLookup(
            _string_by_id_lookup={
                28: RichString(_value="staredit\\wav\\monitor humming.1.wav"),
                43: RichString(_value="staredit\\wav\\monitor humming.2.wav"),
                44: RichString(_value="staredit\\wav\\monitor humming.3.wav"),
            },
            _id_by_string_lookup={
                "staredit\\wav\\monitor humming.1.wav": 28,
                "staredit\\wav\\monitor humming.2.wav": 43,
                "staredit\\wav\\monitor humming.3.wav": 44,
            },
        ),
        _rich_mrgn_lookup=RichMrgnLookup(
            _location_by_id_lookup={}, _id_by_location_lookup={}
        ),
        _rich_swnm_lookup=RichSwnmLookup(
            _switch_by_id_lookup={}, _id_by_switch_lookup={}
        ),
    )


@pytest.fixture
def real_rich_chk_encode_context(real_decoded_wav) -> RichChkEncodeContext:
    # the lookups are based on the real Switch names data in the CHK
    return RichChkEncodeContext(
        _rich_str_lookup=RichStrLookup(
            _string_by_id_lookup={
                28: RichString(_value="staredit\\wav\\monitor humming.1.wav"),
                43: RichString(_value="staredit\\wav\\monitor humming.2.wav"),
                44: RichString(_value="staredit\\wav\\monitor humming.3.wav"),
            },
            _id_by_string_lookup={
                "staredit\\wav\\monitor humming.1.wav": 28,
                "staredit\\wav\\monitor humming.2.wav": 43,
                "staredit\\wav\\monitor humming.3.wav": 44,
            },
        ),
        _rich_mrgn_lookup=RichMrgnLookup(
            _location_by_id_lookup={}, _id_by_location_lookup={}
        ),
        _rich_swnm_lookup=RichSwnmLookup(
            _switch_by_id_lookup={}, _id_by_switch_lookup={}
        ),
        _rich_cuwp_lookup=RichCuwpLookup(_cuwp_by_id_lookup={}, _id_by_cuwp_lookup={}),
    )


def test_integration_it_decodes_all_wavs(
    real_decoded_wav, real_rich_chk_decode_context
):
    rich_transcoder = RichChkWavTranscoder()
    rich_wav = rich_transcoder.decode(
        real_decoded_wav, rich_chk_decode_context=real_rich_chk_decode_context
    )
    assert len(rich_wav.wavs) == 3
    assert _EXPECTED_RICH_WAV in rich_wav.wavs


def test_it_encodes_all_wavs():
    rich_transcoder = RichChkWavTranscoder()
    wavs = [
        RichWav(_path_in_chk=RichString(_value="mywav1.wav"), _index=0),
        RichWav(_path_in_chk=RichString(_value="mywav2.wav"), _index=200),
    ]
    rich_wav = RichWavSection(_wavs=wavs)
    rich_encode_context = RichChkEncodeContext(
        _rich_str_lookup=RichStrLookup(
            _string_by_id_lookup={},
            _id_by_string_lookup={
                wavs[0].path_in_chk.value: 28,
                wavs[1].path_in_chk.value: 75,
            },
        ),
        _rich_mrgn_lookup=RichMrgnLookup(
            _location_by_id_lookup={}, _id_by_location_lookup={}
        ),
        _rich_swnm_lookup=RichSwnmLookup(
            _switch_by_id_lookup={}, _id_by_switch_lookup={}
        ),
        _rich_cuwp_lookup=RichCuwpLookup(_cuwp_by_id_lookup={}, _id_by_cuwp_lookup={}),
    )
    decoded_wav = rich_transcoder.encode(
        rich_wav, rich_chk_encode_context=rich_encode_context
    )
    assert len(decoded_wav.wav_string_ids) == MAX_WAV_FILES
    for wav in wavs:
        assert decoded_wav.wav_string_ids[
            wav.index
        ] == rich_encode_context.rich_str_lookup.get_id_by_string(wav.path_in_chk)
    expected_indices_for_wavs = {wav.index for wav in wavs}
    for index, string_id in enumerate(decoded_wav.wav_string_ids):
        if index in expected_indices_for_wavs:
            assert string_id != UNUSED_WAV_STRING_ID
        else:
            assert string_id == UNUSED_WAV_STRING_ID


def test_integration_it_decodes_and_encodes_without_changing_data(
    real_decoded_wav, real_rich_chk_decode_context, real_rich_chk_encode_context
):
    rich_transcoder = RichChkWavTranscoder()
    rich_wav = rich_transcoder.decode(
        real_decoded_wav, rich_chk_decode_context=real_rich_chk_decode_context
    )
    actual_decoded_wav = rich_transcoder.encode(rich_wav, real_rich_chk_encode_context)
    assert actual_decoded_wav == real_decoded_wav
    assert rich_wav == rich_transcoder.decode(
        actual_decoded_wav, rich_chk_decode_context=real_rich_chk_decode_context
    )
