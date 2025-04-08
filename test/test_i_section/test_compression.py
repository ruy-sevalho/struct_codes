from dataclasses import asdict

from pint import Quantity
from pytest import mark
from unit_processing import compare_quantites

from struct_codes.aisc_database import create_aisc_section
from struct_codes.criteria import DesignType, StrengthType
from struct_codes.i_section import DoublySymmetricI
from struct_codes.i_section._compression import (
    BeamCompressionParam,
)
from struct_codes.materials import steel355MPa
from struct_codes.sections import ConstructionType
from struct_codes.units import meter, newton


@mark.parametrize(
    "section, beam_compression_param, design_type, expected_design_strength",
    [
        (
            create_aisc_section("W6X15", steel355MPa, ConstructionType.ROLLED),
            BeamCompressionParam(length_major_axis=1 * meter),
            DesignType.ASD,
            597228.27 * newton,
        ),
    ],
)
def test_w_section_flexural_buckling_major_axis_calc_memory_2016(
    section: DoublySymmetricI,
    beam_compression_param: BeamCompressionParam,
    design_type: DesignType,
    expected_design_strength: Quantity,
):
    beam = asdict(beam_compression_param)
    ds = (
        section.compression(**beam, design_type=design_type)
        .criteria[StrengthType.FLEXURAL_BUCKLING_MAJOR_AXIS]
        .design_strength
    )
    compare_quantites(ds, expected_design_strength)


@mark.parametrize(
    "section, beam_compression_param, design_type, expected_design_strength",
    [
        (
            create_aisc_section("W6X15", steel355MPa, ConstructionType.ROLLED),
            BeamCompressionParam(length_major_axis=1 * meter),
            DesignType.ASD,
            575092.947 * newton,
        ),
    ],
)
def test_w_section_flexural_buckling_minor_axis_calc_memory_2016(
    section: DoublySymmetricI,
    beam_compression_param: BeamCompressionParam,
    design_type: DesignType,
    expected_design_strength: Quantity,
):
    beam = asdict(beam_compression_param)
    ds = (
        section.compression(**beam, design_type=design_type)
        .criteria[StrengthType.FLEXURAL_BUCKLING_MINOR_AXIS]
        .design_strength
    )
    compare_quantites(ds, expected_design_strength)


@mark.parametrize(
    "section, beam_compression_param, design_type, expected_design_strength",
    [
        (
            create_aisc_section("W6X15", steel355MPa, ConstructionType.ROLLED),
            BeamCompressionParam(length_major_axis=1 * meter),
            DesignType.ASD,
            575811.9028 * newton,
        ),
    ],
)
def test_w_section_torsional_calc_memory_2016(
    section: DoublySymmetricI,
    beam_compression_param: BeamCompressionParam,
    design_type: DesignType,
    expected_design_strength: Quantity,
):
    beam = asdict(beam_compression_param)
    ds = (
        section.compression(**beam, design_type=design_type)
        .criteria[StrengthType.TORSIONAL_BUCKLING]
        .design_strength
    )
    compare_quantites(ds, expected_design_strength)
