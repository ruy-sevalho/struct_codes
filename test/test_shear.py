from pytest import approx, mark
from unit_processing import simplify_dataclass

from struct_codes._shear import WebShearCalculationMemory2016
from struct_codes.aisc_database import create_aisc_section
from struct_codes.criteria import DesignType, StrengthType
from struct_codes.i_section import DoublySymmetricI
from struct_codes.materials import steel250MPa, steel355MPa
from struct_codes.sections import ConstructionType
from struct_codes.units import newton


@mark.parametrize(
    "section, design_type, expected_shear_yielding_calc_memory",
    [
        (
            create_aisc_section("W44X335", steel355MPa, ConstructionType.ROLLED),
            DesignType.ASD,
            WebShearCalculationMemory2016(
                nominal_strength=6250272 * newton,
                design_strength=4166848 * newton,
                web_shear_strength_coefficient=1,
            ),
        ),
        (
            create_aisc_section("W6X15", steel250MPa, ConstructionType.ROLLED),
            DesignType.LRFD,
            WebShearCalculationMemory2016(
                nominal_strength=133152 * newton,
                design_strength=133152 * newton,
                web_shear_strength_coefficient=1,
            ),
        ),
    ],
)
def test_w_section_web_shear_calc_memory_2016(
    section: DoublySymmetricI,
    design_type: DesignType,
    expected_shear_yielding_calc_memory: WebShearCalculationMemory2016,
):
    calc_memory = (
        section.shear_major_axis(
            design_type=design_type,
        )
        .criteria[StrengthType.WEB_SHEAR]
        .calculation_memory
    )
    assert simplify_dataclass(calc_memory) == approx(
        simplify_dataclass(expected_shear_yielding_calc_memory)
    )
