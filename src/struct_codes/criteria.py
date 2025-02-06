from enum import Enum

from pint import Quantity


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
