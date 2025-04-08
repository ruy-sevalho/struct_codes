from pint import Quantity
from pytest import mark
from unit_processing import compare_quantites 

from struct_codes.aisc_database import create_aisc_section
from struct_codes.criteria import DesignType, StrengthType

from struct_codes.materials import steel355MPa
from struct_codes.sections import ConstructionType, Section
from struct_codes.units import newton


@mark.parametrize(
    "section, design_type, expected_design_strength",
    [
        (
            create_aisc_section("W6X15", steel355MPa, ConstructionType.ROLLED),
            DesignType.ASD,
            607_964.0719 * newton,
        )
    ],
)
def test_tension_yield_calc_memory(
    section: Section,
    design_type: DesignType,
    expected_design_strength: Quantity,
):
    calc = section.tension(design_type=design_type)
    ds = calc.criteria[StrengthType.YIELD].design_strength
    compare_quantites(ds, expected_design_strength)


@mark.parametrize(
    "section, design_type, expected_design_strength",
    [
        (
            create_aisc_section("W6X15", steel355MPa, ConstructionType.ROLLED),
            DesignType.ASD,
            715_000 * newton * newton,
        )
    ],
)
def test_tension_ultimate_calc_memory(
    section: Section,
    design_type: DesignType,
    expected_design_strength: Quantity,
):
    calc = section.tension(design_type=design_type)
    ds = calc.criteria[StrengthType.ULTIMATE].design_strength
    compare_quantites(ds, expected_design_strength)
