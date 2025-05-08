from decimal import Decimal

from .....model.richchk.unis.unit_id import UnitId
from .....util import logger


class UnitHitpointsTranscoder:
    _LOG = logger.get_logger("UnitHitpointsTranscoder")
    _HITPOINTS_CONVERSION_RATE = 256

    @classmethod
    def decode_hitpoints(cls, unit_id: UnitId, hitpoints_before_decode: int) -> Decimal:
        maybe_remainder = hitpoints_before_decode % cls._HITPOINTS_CONVERSION_RATE
        if maybe_remainder:
            cls._LOG.warning(
                f"Unit {unit_id} "
                f"had fractional hitpoints of {maybe_remainder} / {cls._HITPOINTS_CONVERSION_RATE} "
                f"due to decoded hitpoints {hitpoints_before_decode}"
                f"not being an even multiple of 256"
            )
        actual_hitpoints = Decimal(hitpoints_before_decode) / Decimal(256)
        return actual_hitpoints

    @classmethod
    def encode_hitpoints(cls, encoded_hitpoints: Decimal) -> int:
        # this is a lossy conversion, should add logging to monitor this
        return int(Decimal(encoded_hitpoints) * Decimal(cls._HITPOINTS_CONVERSION_RATE))
