"""Search RichMrgn for locations by their name or ID."""

import difflib
from typing import Optional, TypeVar

from richchk.model.chk.decoded_chk_section import DecodedChkSection
from richchk.model.richchk.mrgn.rich_location import RichLocation
from richchk.model.richchk.mrgn.rich_mrgn_section import RichMrgnSection
from richchk.model.richchk.rich_chk_section import RichChkSection

_T = TypeVar("_T", bound=RichChkSection, covariant=True)
_U = TypeVar("_U", bound=DecodedChkSection, covariant=True)


class MrgnSearchUtil:
    @staticmethod
    def find_location_by_name(
        location_name: str, mrgn: RichMrgnSection, ignorecase: bool = True
    ) -> Optional[RichLocation]:
        """Finds the only location matching the exact name.

        Throws if more than 1 location matches the exact name.
        """
        exact_matches = []
        for loc in mrgn.locations:
            name1, name2 = MrgnSearchUtil._get_location_names_for_comparison(
                location_name, loc.custom_location_name.value, ignorecase=ignorecase
            )
            if name1 == name2:
                exact_matches.append(loc)
        if len(exact_matches) > 1:
            msg = (
                f"There were more than 1 locations matching the exact name!  "
                f"Location name: {location_name} but had the following matches: {exact_matches}"
            )
            raise ValueError(msg)
        if len(exact_matches) == 1:
            return exact_matches[0]
        return None

    @staticmethod
    def find_location_by_fuzzy_search(
        location_name: str,
        mrgn: RichMrgnSection,
        ignorecase: bool = True,
        min_similarity: float = 0.20,
    ) -> RichLocation:
        """Fuzzy search for the location with the closest name in the MRGN.

        This will always return a result for the location with the highest similarity.
        If no location is greater than `min_similarity`, the method will throw.
        """
        locs_by_similarity = []
        for loc in mrgn.locations:
            name1, name2 = MrgnSearchUtil._get_location_names_for_comparison(
                location_name, loc.custom_location_name.value, ignorecase=ignorecase
            )
            matcher = difflib.SequenceMatcher(None, name1, name2)
            similarity = matcher.ratio()
            locs_by_similarity.append((similarity, loc))
        best_match = max(locs_by_similarity, key=lambda x: x[0])
        if best_match[0] >= min_similarity:
            return best_match[1]
        else:
            msg = (
                f"The best match for {location_name} is {best_match[1].custom_location_name.value} "
                f"whose similarity score of {best_match[0]} is lower than {min_similarity}"
            )
            raise ValueError(msg)

    @staticmethod
    def _get_location_names_for_comparison(
        loc1_name: str, loc2_name: str, ignorecase: bool
    ) -> tuple[str, str]:
        if ignorecase:
            return (
                loc1_name.lower(),
                loc2_name.lower(),
            )
        return loc1_name, loc2_name
