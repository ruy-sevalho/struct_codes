from enum import Enum
from dataclasses import dataclass

from pint import Quantity

from struct_codes.sections import ConstructionType


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
class SlendernessTypes(str, Enum):
    WEB_AXIAL = "web_axial"
    WEB_FLEXURE_MAJOR_AXIS = "web_flexure_major_axis"
    FLANGE_AXIAL = "flange_axial"
    FLANGE_FLEXURE_MAJOR_AXIS = "flange_flexure_major_axis"
    FLANGE_FLEXURE_MINOR_AXIS = "flange_flexure_minor_axis"


@dataclass
class DefaultSlenderness:
    web_axial: Slenderness
    web_flexure_major_axis: Slenderness
    flange_axial: Slenderness
    flange_flexure_major_axis: Slenderness
    flange_flexure_minor_axis: Slenderness


@dataclass
class DefaultSlendernessCalculation2016:
    construction: ConstructionType
    web_ratio: float
    flange_ratio: float
    modulus_linear: Quantity
    yield_strength: Quantity

    @property
    def kc_coeficient(self):
        return kc_coefficient(heigth_to_thickness_ratio=self.web_ratio)

    @property
    def _flange_axial_built_up_limit_ratio(self) -> float:
        return axial_built_up_flanges_limit_ratio(
            modulus_linear=self.modulus_linear,
            yield_strength=self.yield_strength,
            kc_coefficient=self.kc_coeficient,
        )

    @property
    def _flange_axial_rolled_limit_ratio(self) -> float:
        return axial_rolled_flanges_limit_ratio(
            modulus_linear=self.modulus_linear,
            yield_strength=self.yield_strength,
        )

    @property
    def _flange_axial_limit(self) -> float:
        table = {
            ConstructionType.BUILT_UP: self._flange_axial_built_up_limit_ratio,
            ConstructionType.ROLLED: self._flange_axial_rolled_limit_ratio,
        }
        return table[self.construction]

    @property
    def _web_axial_slender_limit(self) -> float:
        return axial_doubly_symmetric_web_limit(
            modulus_linear=self.modulus_linear,
            yield_strength=self.yield_strength,
        )

    @property
    def _flange_flexural_rolled_compact_limit(self) -> float:
        return flexural_rolled_i_channel_tees_flange_compact_limit(
            modulus_linear=self.modulus_linear,
            yield_strength=self.yield_strength,
        )

    @property
    def _flange_flexural_rolled_slender_limit(self) -> float:
        return flexural_rolled_i_channel_tees_flange_slender_limit(
            modulus_linear=self.modulus_linear,
            yield_strength=self.yield_strength,
        )

    @property
    def _flange_flexural_built_up_compact_limit_ratio(self) -> float:
        return flexural_built_up_i_flange_compact_limit(
            modulus_linear=self.modulus_linear,
            yield_strength=self.yield_strength,
        )

    @property
    def _flange_flexural_built_up_slender_limit_ratio(self) -> float:
        return flexural_built_up_i_flange_slender_limit(
            modulus_linear=self.modulus_linear,
            yield_strength=self.yield_strength,
            kc_coefficient=self.kc_coeficient,
        )

    @property
    def _flange_flexural_compact_limit(self) -> Slenderness:
        table = {
            ConstructionType.ROLLED: self._flange_flexural_rolled_compact_limit,
            ConstructionType.BUILT_UP: self._flange_flexural_built_up_compact_limit_ratio,
        }
        return table[self.construction]

    @property
    def _flange_flexural_slender_limit(self) -> Slenderness:
        table = {
            ConstructionType.ROLLED: self._flange_flexural_rolled_slender_limit,
            ConstructionType.BUILT_UP: self._flange_flexural_built_up_slender_limit_ratio,
        }
        return table[self.construction]

    @property
    def _web_flexural_slender_limit(self) -> Slenderness:
        return flexural_doubly_symmetric_web_slender_limit_ratio(
            modulus_linear=self.modulus_linear,
            yield_strength=self.yield_strength,
        )

    @property
    def _flange_flexural_slender_limit(self) -> float:
        table = {
            ConstructionType.BUILT_UP: self._flange_flexural_built_up_slender_limit_ratio,
            ConstructionType.ROLLED: self._flange_flexural_rolled_slender_limit,
        }
        return table[self.construction]

    @property
    def _web_flexural_compact_limit(self) -> Slenderness:
        return flexural_doubly_symmetric_web_compact_limit(
            modulus_linear=self.modulus_linear,
            yield_strength=self.yield_strength,
        )

    @property
    def web_axial(self) -> Slenderness:
        return axial_slenderness_per_element(
            ratio=self.web_ratio, limit=self._web_axial_slender_limit
        )

    @property
    def web_flexural(self) -> Slenderness:
        return flexural_slenderness_per_element(
            limit_slender=self._web_flexural_slender_limit,
            limit_compact=self._web_flexural_compact_limit,
            ratio=self.web_ratio,
        )

    @property
    def flange_axial(self) -> Slenderness:
        return axial_slenderness_per_element(
            ratio=self.flange_ratio, limit=self._flange_axial_limit
        )

    @property
    def flange_flexural_major_axis(self) -> Slenderness:
        return flexural_slenderness_per_element(
            limit_slender=self._flange_flexural_slender_limit,
            limit_compact=self._flange_flexural_compact_limit,
            ratio=self.flange_ratio,
        )

    @property
    def flange_flexural_minor_axis(self) -> Slenderness:
        return flexural_slenderness_per_element(
            limit_slender=self._flange_flexural_rolled_slender_limit,
            limit_compact=self._flange_flexural_rolled_compact_limit,
            ratio=self.flange_ratio,
        )


def _is_slender(
    lamdba_ratio: float,
    lambda_limit: float,
    yield_stess: Quantity,
    critical_stress: Quantity,
):
    if lamdba_ratio > lambda_limit * (yield_stess / critical_stress) ** 0.5:
        raise NotImplementedError("Chapter E section 7 not implemented")
    return False
