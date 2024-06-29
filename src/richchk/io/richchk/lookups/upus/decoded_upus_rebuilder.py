"""Rebuild a new DecodedUpusSection from a RichUprpSection."""

from .....model.chk.uprp.uprp_constants import MAX_CUWP_SLOTS
from .....model.chk.upus.decoded_upus_section import DecodedUpusSection
from .....model.richchk.uprp.rich_uprp_section import RichUprpSection


class DecodedUpusRebuilder:
    @classmethod
    def rebuild_upus_from_rich_uprp(
        cls, rich_uprp: RichUprpSection
    ) -> DecodedUpusSection:
        cuwp_used = [0] * MAX_CUWP_SLOTS
        for cuwp in rich_uprp.cuwp_slots:
            assert cuwp.index is not None
            assert cuwp.index > 0
            cuwp_used[cuwp.index - 1] = 1
        return DecodedUpusSection(_cuwp_slots_used=cuwp_used)
