from pint import Quantity
from pytest import approx, mark
from unit_processing import simplify_dataclass

from struct_codes.aisc_database import create_aisc_section
from struct_codes.criteria import DesignType, StrengthType
from struct_codes.i_section import DoublySymmetricI
from struct_codes.i_section._flexure import (
    LateralTorsionalBucklingCalculationMemory,
    YieldingMomentCalculationMemory,
)
from struct_codes.materials import steel250MPa, steel355MPa
from struct_codes.sections import ConstructionType
from struct_codes.units import meter, newton


@mark.parametrize(
    "section, design_type, expected_flexural_yielding_calc_memory",
    [
        (
            create_aisc_section("W44X335", steel355MPa, ConstructionType.ROLLED),
            DesignType.ASD,
            YieldingMomentCalculationMemory(
                nominal_strength=9407500 * newton * meter,
                design_strength=5633233.533 * newton * meter,
            ),
        ),
        (
            create_aisc_section("W6X15", steel250MPa, ConstructionType.ROLLED),
            DesignType.ASD,
            YieldingMomentCalculationMemory(
                nominal_strength=44250 * newton * meter,
                design_strength=26497.00599 * newton * meter,
            ),
        ),
    ],
)
def test_w_section_flexural_yielding_major_axis_calc_memory_2016(
    section: DoublySymmetricI,
    design_type: DesignType,
    expected_flexural_yielding_calc_memory: YieldingMomentCalculationMemory,
):
    length = 1 * meter
    calc_memory = (
        section.flexure_major_axis(
            length=length,
            design_type=design_type,
        )
        .criteria[StrengthType.YIELD]
        .calculation_memory
    )
    assert simplify_dataclass(calc_memory) == approx(
        simplify_dataclass(expected_flexural_yielding_calc_memory)
    )


@mark.parametrize(
    "section, design_type, expected_flexural_yielding_calc_memory",
    [
        (
            create_aisc_section("W44X335", steel355MPa, ConstructionType.ROLLED),
            DesignType.ASD,
            YieldingMomentCalculationMemory(
                nominal_strength=1373850 * newton * meter,
                design_strength=822664.6707 * newton * meter,
            ),
        ),
        (
            create_aisc_section("W6X15", steel250MPa, ConstructionType.ROLLED),
            DesignType.ASD,
            YieldingMomentCalculationMemory(
                nominal_strength=19450 * newton * meter,
                design_strength=11646.70659 * newton * meter,
            ),
        ),
    ],
)
def test_w_section_flexural_yielding_minor_axis_calc_memory_2016(
    section: DoublySymmetricI,
    design_type: DesignType,
    expected_flexural_yielding_calc_memory: YieldingMomentCalculationMemory,
):
    calc_memory = (
        section.flexure_minor_axis(
            design_type=design_type,
        )
        .criteria[StrengthType.YIELD]
        .calculation_memory
    )
    assert simplify_dataclass(calc_memory) == approx(
        simplify_dataclass(expected_flexural_yielding_calc_memory)
    )


@mark.parametrize(
    "section, length, lateral_torsional_buckling_modification_factor, design_type, expected_flexural_yielding_calc_memory",
    [
        (
            create_aisc_section("W6X15", steel250MPa, ConstructionType.ROLLED),
            2.1 * meter,
            1.0,
            DesignType.ASD,
            LateralTorsionalBucklingCalculationMemory(
                limiting_buckling_length=6.44555 * meter,
                limiting_yield_length=1.83191568 * meter,
                nominal_strength=43295.5932 * newton * meter,
                design_strength=25925.50491 * newton * meter,
            ),
        ),
        (
            create_aisc_section("W6X15", steel250MPa, ConstructionType.ROLLED),
            7.0 * meter,
            1.0,
            DesignType.ASD,
            LateralTorsionalBucklingCalculationMemory(
                limiting_buckling_length=6.44555 * meter,
                limiting_yield_length=1.83191568 * meter,
                nominal_strength=25145.29 * newton * meter,
                design_strength=15057.06275 * newton * meter,
            ),
        ),
    ],
)
def test_w_section_major_axis_lateral_torsional_buckling_calc_memory_2016(
    section: DoublySymmetricI,
    length: Quantity,
    lateral_torsional_buckling_modification_factor: float,
    design_type: DesignType,
    expected_flexural_yielding_calc_memory: LateralTorsionalBucklingCalculationMemory,
):
    calc_memory = (
        section.flexure_major_axis(
            length=length,
            lateral_torsional_buckling_modification_factor=lateral_torsional_buckling_modification_factor,
            design_type=design_type,
        )
        .criteria[StrengthType.LATERAL_TORSIONAL_BUCKLING]
        .calculation_memory
    )
    assert simplify_dataclass(calc_memory) == approx(
        simplify_dataclass(expected_flexural_yielding_calc_memory)
    )
