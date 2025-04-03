from enum import Enum


class Slenderness(str, Enum):
    SLENDER = "slender"
    NON_SLENDER = "non_slender"
    COMPACT = "compact"
    NON_COMPACT = "non_compact"


def flexural_slenderness_per_element(
    limit_slender: float, limit_compact: float, ratio: float
) -> Slenderness:
    if ratio < limit_compact:
        return Slenderness.COMPACT
    elif ratio < limit_slender:
        return Slenderness.NON_COMPACT
    else:
        return Slenderness.SLENDER
