from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

from pint import Quantity


class StrengthType(str, Enum):
    WEB_SHEAR = "web_shear"
    FLEXURAL_BUCKLING_MAJOR_AXIS = "flexural_buckling_major_axis"
    FLEXURAL_BUCKLING_MINOR_AXIS = "flexural_buckling_minor_axis"
    TORSIONAL_BUCKLING = "torsional_buckling"
    YIELD = "yield"
    ULTIMATE = "ultimate"
    LATERAL_TORSIONAL_BUCKLING = "lateral_torsional_buckling"
    COMPRESSION_FLANGE_LOCAL_BUCKLING = "compression_flange_local_buckling"
    COMPRESSION_FLANGE_YIELDING = "compression_flange_yielding"
    TENSION_FLANGE_YIELDING = "tension_flange_yielding"


class DesignType(str, Enum):
    ASD = "ASD"
    LRFD = "LRFD"


def calculate_design_strength(
    nominal_strength: Quantity, design_type: DesignType, factor: float | None = None
) -> Quantity:
    default_factor = {DesignType.ASD: 1.67, DesignType.LRFD: 0.9}
    factor = factor or default_factor[design_type]
    calc_function = {
        DesignType.ASD: lambda x, y: x / y,
        DesignType.LRFD: lambda x, y: x * y,
    }
    return calc_function[design_type](nominal_strength, factor)


class StrengthMixin(ABC):
    design_type: DesignType

    asd_factor = 1.67
    lrfd_factor = 0.9

    @property
    @abstractmethod
    def nominal_strength(self) -> Quantity: ...

    @property
    def design_strength(self) -> Quantity:
        table = {DesignType.ASD: self.asd_factor, DesignType.LRFD: self.lrfd_factor}
        return calculate_design_strength(
            nominal_strength=self.nominal_strength,
            design_type=self.design_type,
            factor=table[self.design_type],
        )
