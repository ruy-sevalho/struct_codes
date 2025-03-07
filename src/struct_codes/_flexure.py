from dataclasses import dataclass
import math

from pint import Quantity

from struct_codes.criteria import DesignType, StrengthMixin
from struct_codes.sections import StrengthCalculation


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
    return calculated_moment



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


@dataclass
class YieldingMomentCalculationMemory:
    nominal_strength: Quantity
    design_strength: Quantity


@dataclass
class YieldingMomentCalculation(StrengthMixin):
    plastic_section_modulus: Quantity
    yield_stress: Quantity
    design_type: DesignType

    @property
    def nominal_strength(self):
        return yielding_moment(
            plastic_section_modulus=self.plastic_section_modulus,
            yield_stress=self.yield_stress,
        )

    @property
    def calculation_memory(self):
        return YieldingMomentCalculationMemory(
            nominal_strength=self.nominal_strength, design_strength=self.design_strength
        )
