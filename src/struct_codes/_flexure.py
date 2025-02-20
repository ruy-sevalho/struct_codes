from dataclasses import dataclass

from pint import Quantity

from struct_codes.criteria import DesignType, StrengthMixin
from struct_codes.sections import StrengthCalculation


# 2016 - F2-1
def yielding_moment(
    plastic_section_modulus: Quantity, yield_stress: Quantity
) -> Quantity:
    return plastic_section_modulus * yield_stress


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
