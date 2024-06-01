"""Compare numeric values for conditions.

See: http://www.staredit.net/wiki/index.php/Scenario.chk#Numeric_Comparisons
"""

from ......model.richchk.richchk_enum import RichChkEnum


class NumericComparator(RichChkEnum):
    AT_LEAST = (0, "At least")
    AT_MOST = (1, "At most")
    EXACTLY = (10, "Exactly")
