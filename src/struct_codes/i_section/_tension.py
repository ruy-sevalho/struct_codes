from dataclasses import dataclass

from struct_codes.criteria import DesignType, Strength
from struct_codes.units import Quantity


@dataclass
class TesionYieldCalculation(Strength):
    gross_area: Quantity
    yield_stress: Quantity
    design_type: DesignType

    @property
    def nominal_strength(self):
        return self.yield_stress * self.gross_area


@dataclass
class TesionUltimateCalculation(Strength):
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
