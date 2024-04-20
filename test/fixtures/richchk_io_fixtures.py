""""""
from chkjson.model.richchk.richchk_decode_context import RichChkDecodeContext
from chkjson.model.richchk.str.rich_str_lookup import RichStrLookup
from chkjson.model.richchk.str.rich_string import RichString


def generate_rich_chk_decode_context():
    return RichChkDecodeContext(
        _rich_str_lookup=RichStrLookup(
            {123: RichString(_value="custom terran marine name")},
            _id_by_string_lookup={"custom terran marine name": 123},
        )
    )


def generate_empty_rich_chk_decode_context():
    return RichChkDecodeContext(
        _rich_str_lookup=RichStrLookup(
            _string_by_id_lookup={},
            _id_by_string_lookup={},
        )
    )
