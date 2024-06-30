from richchk.model.chk.str.decoded_str_section import DecodedStrSection


def generate_decoded_str_section() -> DecodedStrSection:
    return DecodedStrSection(
        # the first offset points to where the last offset ends in bytes
        # first 2 bytes are number of strings, next 2 bytes is the offset
        # so "a" starts at byte position 4 (0 indexed)
        _number_of_strings=1,
        _string_offsets=[4],
        _strings=["a"],
    )
