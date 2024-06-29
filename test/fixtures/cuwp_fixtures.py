""""""
from typing import Optional

from richchk.model.richchk.uprp.rich_cuwp_slot import RichCuwpSlot


def generate_cuwp_slot(index: Optional[int] = None) -> RichCuwpSlot:
    return RichCuwpSlot(
        _hitpoints_percentage=100,
        _shieldpoints_percentage=100,
        _energypoints_percentage=100,
        _resource_amount=0,
        _units_in_hangar=0,
        _index=index,
    )
