from dataclasses import dataclass

from struct_codes.criteria import DesignType, StrengthMixin
from struct_codes.units import Quantity


@dataclass
class TensionYieldCalculationMemory:
    nominal_strength: Quantity
    design_strength: Quantity


@dataclass
class TensionUltimateCalculationMemory:
    net_effective_area: Quantity
    nominal_strength: Quantity
    design_strength: Quantity


@dataclass
class TensionCalculationMemory:
    nominal_yielding_strength: Quantity
    nominal_ultimate_strength: Quantity
    yielding_strength: Quantity
    ultimate_strength: Quantity
    design_strength: Quantity
    design_type: DesignType


@dataclass
class TesionYieldCalculation(StrengthMixin):
    gross_area: Quantity
    yield_stress: Quantity
    design_type: DesignType

    @property
    def nominal_strength(self):
        return self.yield_stress * self.gross_area

    @property
    def calculation_memory(self):
        return TensionYieldCalculationMemory(
            nominal_strength=self.nominal_strength, design_strength=self.design_strength
        )


@dataclass
class TesionUltimateCalculation(StrengthMixin):
    net_area: Quantity
    ultimate_stress: Quantity
    design_type: DesignType
    shear_lag_factor: float = 1.0

    asd_factor = 2
    lrfd_factor = 0.75

    @property
    def nominal_strength(self):
        return self.net_effective_area * self.ultimate_stress

    @property
    def net_effective_area(self):
        return self.net_area * self.shear_lag_factor

    @property
    def calculation_memory(self):
        return TensionUltimateCalculationMemory(
            net_effective_area=self.net_effective_area,
            nominal_strength=self.nominal_strength,
            design_strength=self.design_strength,
        )
