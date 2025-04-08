from pint import Quantity
from pytest import mark
from unit_processing import compare_quantites

from struct_codes.aisc_database import create_aisc_section
from struct_codes.criteria import DesignType, StrengthType
from struct_codes.i_section import DoublySymmetricI
from struct_codes.materials import steel250MPa, steel355MPa
from struct_codes.sections import ConstructionType
from struct_codes.units import meter, newton


@mark.parametrize(
    "section, design_type, expected_design_strength",
    [
        (
            create_aisc_section("W44X335", steel355MPa, ConstructionType.ROLLED),
            DesignType.ASD,
            5633233.533 * newton * meter,
        ),
        (
            create_aisc_section("W6X15", steel250MPa, ConstructionType.ROLLED),
            DesignType.ASD,
            26497.00599 * newton * meter,
        ),
    ],
)
def test_w_section_flexural_yielding_major_axis_calc_memory_2016(
    section: DoublySymmetricI,
    design_type: DesignType,
    expected_design_strength: Quantity,
):
    length = 1 * meter
    ds = (
        section.flexure_major_axis(
            length=length,
            design_type=design_type,
        )
        .criteria[StrengthType.YIELD]
        .design_strength
    )
    compare_quantites(ds, expected_design_strength)


@mark.parametrize(
    "section, design_type, expected_design_strength",
    [
        (
            create_aisc_section("W44X335", steel355MPa, ConstructionType.ROLLED),
            DesignType.ASD,
            822664.6707 * newton * meter,
        ),
        (
            create_aisc_section("W6X15", steel250MPa, ConstructionType.ROLLED),
            DesignType.ASD,
            11646.70659 * newton * meter,
        ),
    ],
)
def test_w_section_flexural_yielding_minor_axis_calc_memory_2016(
    section: DoublySymmetricI,
    design_type: DesignType,
    expected_design_strength: Quantity,
):
    ds = (
        section.flexure_minor_axis(
            design_type=design_type,
        )
        .criteria[StrengthType.YIELD]
        .design_strength
    )
    compare_quantites(ds, expected_design_strength)


@mark.parametrize(
    "section, length, lateral_torsional_buckling_modification_factor, design_type, expected_design_strength",
    [
        (
            create_aisc_section("W6X15", steel250MPa, ConstructionType.ROLLED),
            2.1 * meter,
            1.0,
            DesignType.ASD,
            25925.50491 * newton * meter,
        ),
        (
            create_aisc_section("W6X15", steel250MPa, ConstructionType.ROLLED),
            7.0 * meter,
            1.0,
            DesignType.ASD,
            15057.06275 * newton * meter,
        ),
    ],
)
def test_w_section_major_axis_lateral_torsional_buckling_calc_memory_2016(
    section: DoublySymmetricI,
    length: Quantity,
    lateral_torsional_buckling_modification_factor: float,
    design_type: DesignType,
    expected_design_strength: Quantity,
):
    ds = (
        section.flexure_major_axis(
            length=length,
            lateral_torsional_buckling_modification_factor=lateral_torsional_buckling_modification_factor,
            design_type=design_type,
        )
        .criteria[StrengthType.LATERAL_TORSIONAL_BUCKLING]
        .design_strength
    )
    compare_quantites(ds, expected_design_strength)
