from dataclasses import dataclass

from struct_codes.criteria import DesignType, StrengthMixin, calculate_design_strength
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


@dataclass
class TensionCalculation2016:
    """CHAPTER D DESIGN OF MEMBERS FOR TENSION"""

    net_area: Quantity
    gross_area: Quantity
    yield_stress: Quantity
    ultimate_stress: Quantity
    shear_lag_factor: float = 1.0
    design_type: DesignType = DesignType.ASD

    @property
    def strength(self):
        return min(self.yielding_strength, self.ultimate_strength)

    @property
    def nominal_yielding_strength(self):
        return self.yield_stress * self.gross_area

    @property
    def nominal_ultimate_strength(self):
        return self.net_effective_area * self.ultimate_stress

    @property
    def net_effective_area(self):
        return self.net_area * self.shear_lag_factor

    @property
    def yielding_strength(self):
        return calculate_design_strength(
            nominal_strength=self.nominal_yielding_strength,
            design_type=self.design_type,
        )

    @property
    def ultimate_strength(self):
        factor_table = {DesignType.ASD: 2.0, DesignType.LRFD: 0.75}
        return calculate_design_strength(
            nominal_strength=self.nominal_ultimate_strength,
            design_type=self.design_type,
            factor=factor_table[self.design_type],
        )

    @property
    def calculation_memory(self):
        return TensionCalculationMemory(
            nominal_yielding_strength=self.nominal_yielding_strength,
            nominal_ultimate_strength=self.nominal_ultimate_strength,
            yielding_strength=self.yielding_strength,
            ultimate_strength=self.ultimate_strength,
            design_strength=self.strength,
            design_type=self.design_type,
        )
