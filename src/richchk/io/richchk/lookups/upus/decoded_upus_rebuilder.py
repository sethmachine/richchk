"""Rebuild a new DecodedUpusSection from a RichUprpSection."""

from typing import Any, cast

from .....model.chk.uprp.uprp_constants import MAX_CUWP_SLOTS
from .....model.chk.upus.decoded_upus_section import DecodedUpusSection
from .....model.richchk.uprp.rich_uprp_section import RichUprpSection

_upus_rebuild_cache: dict[Any, Any] = {}  # id(rich_uprp) → DecodedUpusSection


class DecodedUpusRebuilder:
    @classmethod
    def rebuild_upus_from_rich_uprp(
        cls, rich_uprp: RichUprpSection
    ) -> DecodedUpusSection:
        cache_key = id(rich_uprp)
        cached = _upus_rebuild_cache.get(cache_key)
        if cached is not None:
            return cast(DecodedUpusSection, cached)
        cuwp_used = [0] * MAX_CUWP_SLOTS
        for cuwp in rich_uprp.cuwp_slots:
            assert cuwp.index is not None
            assert cuwp.index > 0
            cuwp_used[cuwp.index - 1] = 1
        result = DecodedUpusSection(_cuwp_slots_used=cuwp_used)
        _upus_rebuild_cache[cache_key] = result
        return result
