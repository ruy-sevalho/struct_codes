from dataclasses import asdict

from pytest import approx, mark

from struct_codes.aisc_database import create_aisc_section
from struct_codes.definitions import ConstructionType, Section_2016
from struct_codes.i_section import (
    DoublySymmetricSlenderness,
    DoublySymmetricSlendernessCalcMemory,
)
from struct_codes.materials import steel355MPa
from struct_codes.slenderness import Slenderness


@mark.parametrize(
    "section, expected_slenderness",
    [
        (
            create_aisc_section("W6X15", steel355MPa, ConstructionType.ROLLED),
            DoublySymmetricSlenderness(
                web_axial=Slenderness.NON_SLENDER,
                web_flexure_major_axis=Slenderness.COMPACT,
                flange_axial=Slenderness.NON_SLENDER,
                flange_flexure_major_axis=Slenderness.NON_COMPACT,
                flange_flexure_minor_axis=Slenderness.NON_COMPACT,
            ),
        )
    ],
)
def test_slenderness(section: Section_2016, expected_slenderness):
    slenderness = section.slenderness_2016
    assert slenderness == expected_slenderness


@mark.parametrize(
    "section, expected_slenderness_calc_memory",
    [
        (
            create_aisc_section("W6X15", steel355MPa, ConstructionType.ROLLED),
            DoublySymmetricSlendernessCalcMemory(
                web_ratio=21.6,
                flange_ratio=11.5,
                web_axial_slender_limit=35.36609341,
                web_axial_slenderness=Slenderness.NON_SLENDER,
                web_flexural_compact_limit=89.2459807,
                web_flexural_slender_limit=135.293109,
                web_flexural_slenderness=Slenderness.COMPACT,
                flange_axial_slender_limit=13.29195457,
                flange_axial_slenderness=Slenderness.NON_SLENDER,
                flange_flexural_major_axis_compact_limit=9.019540602,
                flange_flexural_major_axis_slender_limit=23.73563316,
                flange_flexural_major_axis_slenderness=Slenderness.NON_COMPACT,
                flange_flexural_minor_axis_compact_limit=9.019540602,
                flange_flexural_minor_axis_slender_limit=23.73563316,
                flange_flexural_minor_axis_slenderness=Slenderness.NON_COMPACT,
            ),
        )
    ],
)
def test_slenderness_calc_memory(
    section: Section_2016,
    expected_slenderness_calc_memory: DoublySymmetricSlendernessCalcMemory,
):
    slenderness_calc_memory = section.slenderness_calc_memory_2016
    assert asdict(slenderness_calc_memory) == approx(
        asdict(expected_slenderness_calc_memory)
    )
