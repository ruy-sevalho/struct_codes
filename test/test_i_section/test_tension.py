from pytest import approx, mark
from unit_processing import simplify_dataclass

from struct_codes.aisc_database import create_aisc_section
from struct_codes.criteria import DesignType, StrengthType
from struct_codes.i_section._tension import (
    TensionUltimateCalculationMemory,
    TensionYieldCalculationMemory,
)
from struct_codes.materials import steel355MPa
from struct_codes.sections import ConstructionType, Section
from struct_codes.units import millimeter, newton


@mark.parametrize(
    "section, design_type, expected_calc_memory",
    [
        (
            create_aisc_section("W6X15", steel355MPa, ConstructionType.ROLLED),
            DesignType.ASD,
            TensionYieldCalculationMemory(
                nominal_strength=1_015_300 * newton,
                design_strength=607_964.0719 * newton,
            ),
        )
    ],
)
def test_tension_yield_calc_memory(
    section: Section,
    design_type: DesignType,
    expected_calc_memory: TensionYieldCalculationMemory,
):
    calc = section.tension(design_type=design_type)
    calc_memory = calc.criteria[StrengthType.YIELD].calculation_memory
    assert simplify_dataclass(calc_memory) == approx(
        simplify_dataclass(expected_calc_memory)
    )


@mark.parametrize(
    "section, design_type, expected_calc_memory",
    [
        (
            create_aisc_section("W6X15", steel355MPa, ConstructionType.ROLLED),
            DesignType.ASD,
            TensionUltimateCalculationMemory(
                net_effective_area=2860 * millimeter**2,
                nominal_strength=1_430_000 * newton,
                design_strength=715_000 * newton * newton,
            ),
        )
    ],
)
def test_tension_ultimate_calc_memory(
    section: Section,
    design_type: DesignType,
    expected_calc_memory: TensionUltimateCalculationMemory,
):
    calc = section.tension(design_type=design_type)
    calc_memory = calc.criteria[StrengthType.ULTIMATE].calculation_memory
    assert simplify_dataclass(calc_memory) == approx(
        simplify_dataclass(expected_calc_memory)
    )
