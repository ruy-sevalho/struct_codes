import math
from dataclasses import dataclass

from pint import Quantity

from struct_codes.criteria import DesignType, Strength


# ed15 360-2016 - F2-1
def yielding_moment(
    plastic_section_modulus: Quantity, yield_stress: Quantity
) -> Quantity:
    return plastic_section_modulus * yield_stress


# ed15 360-2016 F2-2
def flexural_lateral_torsional_buckling_strength_compact_doubly_symmetric_case_b(
    mod_factor: float,
    plastic_moment: Quantity,
    yield_stress: Quantity,
    section_modulus: Quantity,
    length_between_braces: Quantity,
    limiting_length_yield: Quantity,
    limiting_length_torsional_buckling: Quantity,
) -> Quantity:
    l_factor = (length_between_braces - limiting_length_yield) / (
        limiting_length_torsional_buckling - limiting_length_yield
    )
    mp_factor = plastic_moment - 0.7 * yield_stress * section_modulus
    calculated_moment = mod_factor * (plastic_moment - mp_factor * l_factor)
    return min(calculated_moment, plastic_moment)


def flexural_lateral_torsional_buckling_strength_compact_doubly_symmetric_case_c(
    plastic_moment: Quantity,
    section_modulus: Quantity,
    critical_stress: Quantity,
) -> Quantity:
    return min(critical_stress * section_modulus, plastic_moment)


def flexural_lateral_torsional_buckling_critical_stress_compact_doubly_symmetric(
    mod_factor: float,
    length_between_braces: Quantity,
    modulus: Quantity,
    effective_radius_of_gyration: Quantity,
    coefficient_c: float,
    torsional_constant: Quantity,
    section_modulus: Quantity,
    distance_between_flange_centroids: Quantity,
) -> Quantity:
    ratio = (length_between_braces / effective_radius_of_gyration) ** 2
    first_term = (mod_factor * math.pi**2 * modulus) / ratio
    second_term = (
        1
        + 0.078
        * torsional_constant
        * coefficient_c
        / (section_modulus * distance_between_flange_centroids)
        * ratio
    ) ** 0.5
    return first_term * second_term


def limiting_length_yield(
    radius_of_gyration: Quantity, modulus: Quantity, yield_stress: Quantity
) -> Quantity:
    """eq F2-5 aisc 360-16"""

    return 1.76 * radius_of_gyration * (modulus / yield_stress) ** 0.5


def minor_axis_yield(
    yield_stress: Quantity,
    plastic_section_modulus: Quantity,
    elastic_section_modulus: Quantity,
):
    """eq F6-1 aisc 360-16"""
    return min(
        yield_stress * plastic_section_modulus,
        1.6 * elastic_section_modulus * yield_stress,
    )


def limiting_length_lateral_torsional_buckling(
    modulus: Quantity,
    yield_stress: Quantity,
    elastic_section_modulus: Quantity,
    torsional_constant: Quantity,
    effective_radius_of_gyration: Quantity,
    distance_between_centroids: Quantity,
    coefficient_c: float,
) -> Quantity:
    """eq. F2-6 AISC 360-16"""
    ratio = (
        torsional_constant
        * coefficient_c
        / (elastic_section_modulus * distance_between_centroids)
    )
    inner_root = (ratio**2 + 6.76 * (0.7 * yield_stress / modulus) ** 2) ** 0.5
    outer_root = (ratio + inner_root) ** 0.5
    value = (
        1.95
        * effective_radius_of_gyration
        * modulus
        / (0.7 * yield_stress)
        * outer_root
    )
    return value


def effective_radius_of_gyration(
    major_section_modulus: Quantity,
    minor_inertia: Quantity,
    warping_constant: Quantity,
) -> Quantity:
    """eq F2-7 aisc 360-16"""
    return ((minor_inertia * warping_constant) ** 0.5 / major_section_modulus) ** 0.5


def flexural_lateral_torsional_buckling_strength(
    case_b: Quantity | str,
    case_c: Quantity | str,
    length_between_braces: Quantity,
    limiting_length_yield: Quantity,
    limiting_length_torsional_buckling: Quantity,
) -> Quantity | None:
    if length_between_braces <= limiting_length_yield:
        return None
    elif length_between_braces <= limiting_length_torsional_buckling:
        return case_b
    return case_c


@dataclass
class YieldingMomentCalculation16(Strength):
    """AISC 360 2016 F2.1"""

    plastic_section_modulus: Quantity
    yield_stress: Quantity
    design_type: DesignType

    @property
    def nominal_strength(self):
        return yielding_moment(
            plastic_section_modulus=self.plastic_section_modulus,
            yield_stress=self.yield_stress,
        )


@dataclass
class MinorAxisYieldingCalculation2016(Strength):
    yield_stress: Quantity
    plastic_section_modulus: Quantity
    elastic_section_modulus: Quantity
    design_type: DesignType = DesignType.ASD

    @property
    def nominal_strength(self):
        return minor_axis_yield(
            yield_stress=self.yield_stress,
            plastic_section_modulus=self.plastic_section_modulus,
            elastic_section_modulus=self.elastic_section_modulus,
        )


@dataclass
class LateralTorsionalBucklingSectionParam2016:
    plastic_section_modulus: Quantity
    yield_stress: Quantity
    modulus: Quantity
    radius_of_gyration: Quantity
    elastic_section_modulus: Quantity
    minor_axis_inertia: Quantity
    warping_constant: Quantity
    torsional_constant: Quantity
    distance_between_flange_centroids: Quantity
    coefficient_c: float

    @property
    def plastic_moment(self):
        return self.plastic_section_modulus * self.yield_stress

    @property
    def limiting_yield_length(self) -> Quantity:
        return limiting_length_yield(
            radius_of_gyration=self.radius_of_gyration,
            modulus=self.modulus,
            yield_stress=self.yield_stress,
        )

    @property
    def effective_radius_of_gyration(self):
        return effective_radius_of_gyration(
            major_section_modulus=self.elastic_section_modulus,
            minor_inertia=self.minor_axis_inertia,
            warping_constant=self.warping_constant,
        )

    @property
    def limiting_length_lateral_torsional_buckling(self):
        return limiting_length_lateral_torsional_buckling(
            modulus=self.modulus,
            yield_stress=self.yield_stress,
            elastic_section_modulus=self.elastic_section_modulus,
            torsional_constant=self.torsional_constant,
            effective_radius_of_gyration=self.effective_radius_of_gyration,
            distance_between_centroids=self.distance_between_flange_centroids,
            coefficient_c=self.coefficient_c,
        )


@dataclass
class LateralTorsionalBucklingCalculation2016(Strength):
    length: Quantity
    modulus: Quantity
    yield_stress: Quantity
    plastic_section_modulus: Quantity
    elastic_section_modulus: Quantity
    distance_between_flange_centroids: Quantity
    torsional_constant: Quantity
    warping_constant: Quantity
    radius_of_gyration: Quantity
    minor_axis_inertia: Quantity
    limiting_length_lateral_torsional_buckling: Quantity
    limiting_yield_length: Quantity
    plastic_moment: Quantity
    effective_radius_of_gyration: Quantity
    modification_factor: float
    coefficient_c: float
    design_type: DesignType = DesignType.ASD

    # @property
    # def plastic_moment(self):
    #     return self.plastic_section_modulus * self.yield_stress

    # @property
    # def limiting_yield_length(self) -> Quantity:
    #     return limiting_length_yield(
    #         radius_of_gyration=self.radius_of_gyration,
    #         modulus=self.modulus,
    #         yield_stress=self.yield_stress,
    #     )

    # @property
    # def effective_radius_of_gyration(self):
    #     return effective_radius_of_gyration(
    #         major_section_modulus=self.elastic_section_modulus,
    #         minor_inertia=self.minor_axis_inertia,
    #         warping_constant=self.warping_constant,
    #     )

    # @property
    # def limiting_length_lateral_torsional_buckling(self):
    #     return limiting_length_lateral_torsional_buckling(
    #         modulus=self.modulus,
    #         yield_stress=self.yield_stress,
    #         elastic_section_modulus=self.elastic_section_modulus,
    #         torsional_constant=self.torsional_constant,
    #         effective_radius_of_gyration=self.effective_radius_of_gyration,
    #         distance_between_centroids=self.distance_between_flange_centroids,
    #         coefficient_c=self.coefficient_c,
    #     )

    @property
    def strength_lateral_torsion_compact_case_b(self) -> Quantity:
        """F2-1 page 103"""
        return flexural_lateral_torsional_buckling_strength_compact_doubly_symmetric_case_b(
            length_between_braces=self.length,
            limiting_length_torsional_buckling=self.limiting_length_lateral_torsional_buckling,
            limiting_length_yield=self.limiting_yield_length,
            mod_factor=self.modification_factor,
            plastic_moment=self.plastic_moment,
            section_modulus=self.elastic_section_modulus,
            yield_stress=self.yield_stress,
        )

    @property
    def critical_stress_lateral_torsional_buckling(self) -> Quantity:
        return flexural_lateral_torsional_buckling_critical_stress_compact_doubly_symmetric(
            mod_factor=self.modification_factor,
            length_between_braces=self.length,
            modulus=self.modulus,
            coefficient_c=self.coefficient_c,
            distance_between_flange_centroids=self.distance_between_flange_centroids,
            effective_radius_of_gyration=self.effective_radius_of_gyration,
            section_modulus=self.elastic_section_modulus,
            torsional_constant=self.torsional_constant,
        )

    @property
    def strength_lateral_torsion_compact_case_c(self) -> Quantity:
        return flexural_lateral_torsional_buckling_strength_compact_doubly_symmetric_case_c(
            plastic_moment=self.plastic_moment,
            section_modulus=self.elastic_section_modulus,
            critical_stress=self.critical_stress_lateral_torsional_buckling,
        )

    @property
    def nominal_strength(self):
        return flexural_lateral_torsional_buckling_strength(
            case_b=self.strength_lateral_torsion_compact_case_b,
            case_c=self.strength_lateral_torsion_compact_case_c,
            length_between_braces=self.length,
            limiting_length_yield=self.limiting_yield_length,
            limiting_length_torsional_buckling=self.limiting_length_lateral_torsional_buckling,
        )
