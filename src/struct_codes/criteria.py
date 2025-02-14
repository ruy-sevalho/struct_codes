from dataclasses import dataclass
from enum import Enum

from pint import Quantity


class StrengthType(str, Enum):
    SHEAR = "shear"
    FLEXURAL_BUCKLING_MAJOR_AXIS = "flexural_buckling_major_axis"
    FLEXURAL_BUCKLING_MINOR_AXIS = "flexural_buckling_minor_axis"
    TORSIONAL_BUCKLING = "torsional_buckling"
    YIELD = "yield"
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


@dataclass
class Strengths:
    strengths: tuple[float,]
