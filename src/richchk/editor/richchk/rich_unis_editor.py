"""Edit a RichUnis section, replacing or adding new modified unit settings."""

import copy
import logging
from typing import Optional

from ...model.richchk.unis.rich_unis_section import RichUnisSection
from ...model.richchk.unis.unit_id import UnitId
from ...model.richchk.unis.unit_setting import UnitSetting
from ...util import logger


class RichUnisEditor:
    def __init__(self) -> None:
        self.log: logging.Logger = logger.get_logger(RichUnisEditor.__name__)

    def upsert_all_unit_settings(
        self, unit_settings: list[UnitSetting], unis: RichUnisSection
    ) -> RichUnisSection:
        """Add or replace the unit settings for each modified unit.

        :param self:
        :param unit_settings:
        :param unis:
        :return:
        """
        new_unis = copy.deepcopy(unis)
        for us in unit_settings:
            new_unis = self.upsert_unit_setting(unit_setting=us, unis=new_unis)
        return new_unis

    def upsert_unit_setting(
        self, unit_setting: UnitSetting, unis: RichUnisSection
    ) -> RichUnisSection:
        """Add or replace the unit settings for a modified unit.

        :param unit_setting:
        :param unis:
        :return:
        """
        already_existing_unit_setting = self._find_unit_setting_by_unit_id(
            unit_setting.unit_id, unis
        )
        if already_existing_unit_setting:
            self.log.info(
                f"There is already a unit setting for unit ID {unit_setting.unit_id}.  "
                f"This will be replaced by the new unit setting."
            )
        new_unit_settings = self._append_or_replace_unit_setting(
            unit_setting, unis.unit_settings
        )
        return RichUnisSection(_unit_settings=new_unit_settings)

    def _find_unit_setting_by_unit_id(
        self, unit_id: UnitId, unis: RichUnisSection
    ) -> Optional[UnitSetting]:
        """Find the modified unit setting for a give unit ID.

        :param unit_id:
        :return:
        """
        maybe_unit_settings = [x for x in unis.unit_settings if x.unit_id == unit_id]
        if not maybe_unit_settings:
            return None
        if len(maybe_unit_settings) > 1:
            self.log.error(
                f"There are more than 1 unit settings for unit ID {unit_id} "
                f"(total found {len(maybe_unit_settings)}).  "
                f"Please only have a single unit setting per modified unit."
            )
        return maybe_unit_settings[0]

    def _append_or_replace_unit_setting(
        self, unit_setting: UnitSetting, existing_settings: list[UnitSetting]
    ) -> list[UnitSetting]:
        """Append the new unit setting or replace an existing one.

        :param unit_setting:
        :param existing_settings:
        :return:
        """
        was_unit_setting_replaced = False
        new_settings: list[UnitSetting] = []
        for old_setting in existing_settings:
            if unit_setting.unit_id == old_setting.unit_id:
                # it's possible to run into the same unit id again
                # should we log this?
                new_settings.append(unit_setting)
                was_unit_setting_replaced = True
            else:
                new_settings.append(old_setting)
        if not was_unit_setting_replaced:
            new_settings.append(unit_setting)
        return new_settings
