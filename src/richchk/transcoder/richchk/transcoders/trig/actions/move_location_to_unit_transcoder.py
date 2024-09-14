"""Decode center a location on a unit owned by a player inside another location."""

from ......model.chk.trig.decoded_trigger_action import DecodedTriggerAction
from ......model.richchk.mrgn.rich_location import RichLocation
from ......model.richchk.richchk_decode_context import RichChkDecodeContext
from ......model.richchk.richchk_encode_context import RichChkEncodeContext
from ......model.richchk.trig.actions.move_location_action import MoveLocationAction
from ......model.richchk.trig.player_id import PlayerId
from ......model.richchk.unis.unit_id import UnitId
from ......util import logger
from ...helpers.richchk_enum_transcoder import RichChkEnumTranscoder
from ..rich_trigger_action_transcoder import RichTriggerActionTranscoder
from ..rich_trigger_action_transcoder_factory import (
    _RichTriggerActionRegistrableTranscoder,
)


class RichTriggerMoveLocationToUnitActionTranscoder(
    RichTriggerActionTranscoder[MoveLocationAction, DecodedTriggerAction],
    _RichTriggerActionRegistrableTranscoder,
    trigger_action_id=MoveLocationAction.action_id(),
):
    def __init__(self) -> None:
        self.log = logger.get_logger(
            RichTriggerMoveLocationToUnitActionTranscoder.__name__
        )

    def _decode(
        self,
        decoded_action: DecodedTriggerAction,
        rich_chk_decode_context: RichChkDecodeContext,
    ) -> MoveLocationAction:
        assert decoded_action.action_id == MoveLocationAction.action_id().id
        assert rich_chk_decode_context.rich_mrgn_lookup is not None
        # Location - source location in "Order" and "Move Unit", dest location in "Move Location"
        maybe_destination_location = (
            rich_chk_decode_context.rich_mrgn_lookup.get_location_by_id(
                decoded_action.location_id
            )
        )
        maybe_source_location = (
            rich_chk_decode_context.rich_mrgn_lookup.get_location_by_id(
                decoded_action.second_group
            )
        )
        assert isinstance(maybe_destination_location, RichLocation)
        assert isinstance(maybe_source_location, RichLocation)
        return MoveLocationAction(
            _source_location=maybe_source_location,
            _unit=RichChkEnumTranscoder.decode_enum(
                decoded_action.action_argument_type, UnitId
            ),
            _group=RichChkEnumTranscoder.decode_enum(
                decoded_action.first_group, PlayerId
            ),
            _destination_location=maybe_destination_location,
        )

    def _encode(
        self,
        rich_action: MoveLocationAction,
        rich_chk_encode_context: RichChkEncodeContext,
    ) -> DecodedTriggerAction:
        assert rich_chk_encode_context.rich_mrgn_lookup is not None
        maybe_destination_loc_id = (
            rich_chk_encode_context.rich_mrgn_lookup.get_id_by_location(
                rich_action.destination_location
            )
        )
        maybe_source_loc_id = (
            rich_chk_encode_context.rich_mrgn_lookup.get_id_by_location(
                rich_action.source_location
            )
        )
        assert maybe_destination_loc_id is not None
        assert maybe_source_loc_id is not None
        return DecodedTriggerAction(
            _location_id=maybe_destination_loc_id,
            _text_string_id=0,
            _wav_string_id=0,
            _time=0,
            _first_group=RichChkEnumTranscoder.encode_enum(rich_action.group),
            _second_group=maybe_source_loc_id,
            _action_argument_type=RichChkEnumTranscoder.encode_enum(rich_action.unit),
            _action_id=rich_action.action_id().id,
            _quantifier_or_switch_or_order=0,
            _flags=0,
            _padding=0,
            _mask_flag=0,
        )