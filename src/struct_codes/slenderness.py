from dataclasses import dataclass
from enum import Enum

from struct_codes.units import Quantity


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


def axial_slenderness_per_element(ratio: float, limit: float):
    if ratio < limit:
        return Slenderness.NON_SLENDER
    return Slenderness.SLENDER


def axial_rolled_flanges_limit_ratio(
    modulus_linear: Quantity, yield_strength: Quantity
) -> float:
    """
    TABLE B4.1a Width-to-Thickness Ratios: Compression Elements
    Members Subject to Axial Compression - Case 1
    """
    return 0.56 * (modulus_linear / yield_strength) ** 0.5


def axial_built_up_flanges_limit_ratio(
    modulus_linear: Quantity, yield_strength: Quantity, kc_coefficient: float
) -> float:
    """
    TABLE B4.1a Width-to-Thickness Ratios: Compression Elements
    Members Subject to Axial Compression - Case 2
    """
    return 0.64 * (modulus_linear * kc_coefficient / yield_strength) ** 0.5


def kc_coefficient(heigth_to_thickness_ratio: float):
    """
    TABLE B4.1a Width-to-Thickness Ratios: Compression Elements
    Members Subject to Axial Compression - note [a]
    """
    return min((max((4 / heigth_to_thickness_ratio**0.5, 0.35)), 0.76))


def axial_doubly_symmetric_web_limit(
    modulus_linear: Quantity, yield_strength: Quantity
) -> float:
    """TABLE B4.1a
    Width-to-Thickness Ratios: Compression Elements
    Members Subject to Axial Compression"""
    return 1.49 * (modulus_linear / yield_strength) ** 0.5


def flexural_rolled_i_channel_tees_flange_compact_limit(
    modulus_linear: Quantity, yield_strength: Quantity
) -> float:
    """TABLE B4.1b
    Width-to-Thickness Ratios: Compression Elements
    Members Subject to Flexure"""
    return 0.38 * (modulus_linear / yield_strength) ** 0.5


def flexural_built_up_i_flange_compact_limit(
    modulus_linear: Quantity, yield_strength: Quantity
) -> float:
    """TABLE B4.1b
    Width-to-Thickness Ratios: Compression Elements
    Members Subject to Flexure"""
    return 0.38 * (modulus_linear / yield_strength) ** 0.5


def flexural_rolled_i_channel_tees_flange_slender_limit(
    modulus_linear: Quantity, yield_strength: Quantity
) -> float:
    """TABLE B4.1b
    Width-to-Thickness Ratios: Compression Elements
    Members Subject to Flexure"""
    return (modulus_linear / yield_strength) ** 0.5


def flexural_built_up_i_flange_slender_limit(
    modulus_linear: Quantity, yield_strength: Quantity, kc_coefficient: float
) -> float:
    """TABLE B4.1b
    Width-to-Thickness Ratios: Compression Elements
    Members Subject to Flexure"""
    return 0.95 * (modulus_linear * kc_coefficient / yield_strength) ** 0.5


def flexural_doubly_symmetric_web_compact_limit(
    modulus_linear: Quantity, yield_strength: Quantity
) -> float:
    """TABLE B4.1b
    Width-to-Thickness Ratios: Compression Elements
    Members Subject to Flexure"""
    return 3.76 * (modulus_linear / yield_strength) ** 0.5


def flexural_doubly_symmetric_web_slender_limit_ratio(
    modulus_linear: Quantity, yield_strength: Quantity
) -> float:
    """TABLE B4.1b
    Width-to-Thickness Ratios: Compression Elements
    Members Subject to Flexure"""
    return 5.70 * (modulus_linear / yield_strength) ** 0.5


@dataclass
class AxialSlendernessCalcMemory:
    slender_limit: float
    value: Slenderness


@dataclass
class FlexuralSlendernessCalcMemory:
    compact_non_compact_limit: float
    non_compact_slender_limit: float
    value: Slenderness
