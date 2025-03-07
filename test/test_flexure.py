from pint import Quantity
from pytest import approx, mark
from unit_processing import simplify_dataclass

from struct_codes._flexure import YieldingMomentCalculationMemory
from struct_codes.aisc_database import create_aisc_section
from struct_codes.criteria import DesignType, StrengthType
from struct_codes.i_section import DoublySymmetricI
from struct_codes.materials import steel250MPa, steel355MPa
from struct_codes.sections import ConstructionType
from struct_codes.units import meter, newton


@mark.parametrize(
    "section, length, lateral_torsional_buckling_modification_factor, design_type, expected_flexural_yielding_calc_memory",
    [
        (
            create_aisc_section("W44X335", steel355MPa, ConstructionType.ROLLED),
            1 * meter,
            1.0,
            DesignType.ASD,
            YieldingMomentCalculationMemory(
                nominal_strength=9407500 * newton * meter,
                design_strength=5633233.533 * newton * meter,
            ),
        ),
        (
            create_aisc_section("W6X15", steel250MPa, ConstructionType.ROLLED),
            1 * meter,
            1.0,
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
    length: Quantity,
    lateral_torsional_buckling_modification_factor: float,
    design_type: DesignType,
    expected_flexural_yielding_calc_memory: YieldingMomentCalculationMemory,
):
    f = section.flexure_major_axis(
        length=length,
        lateral_torsional_buckling_modification_factor=lateral_torsional_buckling_modification_factor,
        design_type=design_type,
    )
    s = f.criteria[StrengthType.YIELD]
    calc_memory = (
        section.flexure_major_axis(
            length=length,
            lateral_torsional_buckling_modification_factor=lateral_torsional_buckling_modification_factor,
            design_type=design_type,
        )
        .criteria[StrengthType.YIELD]
        .calculation_memory
    )
    assert simplify_dataclass(calc_memory) == approx(
        simplify_dataclass(expected_flexural_yielding_calc_memory)
    )
