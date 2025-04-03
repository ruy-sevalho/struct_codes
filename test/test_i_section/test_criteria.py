from pint import Quantity
from pytest import approx, mark
from unit_processing import simplify_units

from struct_codes.criteria import DesignType, calculate_design_strength
from struct_codes.units import kilonewton


@mark.parametrize(
    "nominal_strength, design_type, factor, expected_strength",
    [
        (10 * kilonewton, DesignType.ASD, None, 5.9880239528 * kilonewton),
        (10 * kilonewton, DesignType.LRFD, None, 9.0 * kilonewton),
        (10 * kilonewton, DesignType.ASD, 2, 5.0 * kilonewton),
    ],
)
def test_design_strength(
    nominal_strength: Quantity,
    design_type: DesignType,
    factor: float | None,
    expected_strength: Quantity,
):
    assert simplify_units(
        calculate_design_strength(
            nominal_strength=nominal_strength, design_type=design_type, factor=factor
        )
    ) == approx(simplify_units(expected_strength))
