from richchk.model.richchk.richchk_decode_context import RichChkDecodeContext
from richchk.model.richchk.str.rich_str_lookup import RichStrLookup


def generate_empty_rich_chk_decode_context() -> RichChkDecodeContext:
    return RichChkDecodeContext(
        _rich_str_lookup=RichStrLookup(_string_by_id_lookup={}, _id_by_string_lookup={})
    )
