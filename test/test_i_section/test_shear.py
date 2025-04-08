from pint import Quantity
from pytest import mark
from unit_processing import compare_quantites

from struct_codes.aisc_database import create_aisc_section
from struct_codes.criteria import DesignType, StrengthType
from struct_codes.i_section import DoublySymmetricI
from struct_codes.materials import steel250MPa, steel355MPa
from struct_codes.sections import ConstructionType
from struct_codes.units import newton


@mark.parametrize(
    "section, design_type, expected_design_strength",
    [
        (
            create_aisc_section("W44X335", steel355MPa, ConstructionType.ROLLED),
            DesignType.ASD,
            4166848 * newton,
        ),
        (
            create_aisc_section("W6X15", steel250MPa, ConstructionType.ROLLED),
            DesignType.LRFD,
            133152 * newton,
        ),
    ],
)
def test_w_section_web_shear_calc_memory_2016(
    section: DoublySymmetricI,
    design_type: DesignType,
    expected_design_strength: Quantity,
):
    ds = (
        section.shear_major_axis(
            design_type=design_type,
        )
        .criteria[StrengthType.WEB_SHEAR]
        .design_strength
    )
    compare_quantites(ds, expected_design_strength)
