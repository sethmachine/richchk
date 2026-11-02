from .....model.richchk.trig.extended_player_id import AnyPlayerId, _ExtendedPlayerId
from .....model.richchk.trig.player_id import PlayerId
from .richchk_enum_transcoder import RichChkEnumTranscoder


class RichChkPlayerIdTranscoder:
    @classmethod
    def decode(cls, player_id: int) -> AnyPlayerId:
        if RichChkEnumTranscoder.contains_enum_by_id(player_id, PlayerId):
            return RichChkEnumTranscoder.decode_enum(player_id, PlayerId)
        return _ExtendedPlayerId(player_id)

    @classmethod
    def encode(cls, player_id: AnyPlayerId) -> int:
        return player_id.id
