from test.fixtures.cuwp_fixtures import generate_cuwp_slot

import pytest

from richchk.io.richchk.lookups.upus.decoded_upus_rebuilder import DecodedUpusRebuilder
from richchk.model.chk.uprp.uprp_constants import MAX_CUWP_SLOTS
from richchk.model.richchk.uprp.rich_uprp_section import RichUprpSection
from richchk.util.dataclasses_util import build_dataclass_with_fields


@pytest.fixture(scope="function")
def rich_uprp() -> RichUprpSection:
    return RichUprpSection(
        [
            generate_cuwp_slot(index=1),
            build_dataclass_with_fields(
                generate_cuwp_slot(index=7), _hallucinated=True
            ),
            build_dataclass_with_fields(generate_cuwp_slot(index=35), _burrowed=True),
        ]
    )


def test_it_rebuilds_decoded_upus(rich_uprp):
    upus = DecodedUpusRebuilder.rebuild_upus_from_rich_uprp(rich_uprp)
    assert len(upus.cuwp_slots_used) == MAX_CUWP_SLOTS
    expected_used_ids = {cuwp.index for cuwp in rich_uprp.cuwp_slots}
    # CUWP is referenced by 1-based index but stored in 0-based index
    for id_ in range(0, MAX_CUWP_SLOTS):
        if id_ in expected_used_ids:
            assert upus.cuwp_slots_used[id_ - 1] == 1
        else:
            assert upus.cuwp_slots_used[id_ - 1] == 0
