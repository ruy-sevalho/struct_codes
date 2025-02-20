from dataclasses import asdict

from pytest import approx, mark
from unit_processing import simplify_dataclass

from struct_codes._compression import (
    BeamCompressionParam,
    BucklingStrengthCalculationMemory,
)
from struct_codes.aisc_database import create_aisc_section
from struct_codes.criteria import DesignType, StrengthType
from struct_codes.i_section import DoublySymmetricI
from struct_codes.materials import steel355MPa
from struct_codes.sections import ConstructionType
from struct_codes.units import megapascal, meter, newton


@mark.parametrize(
    "section, beam_compression_param, design_type, expected_flexural_buckling_calc_memory",
    [
        (
            create_aisc_section("W6X15", steel355MPa, ConstructionType.ROLLED),
            BeamCompressionParam(length_major_axis=1 * meter),
            DesignType.ASD,
            BucklingStrengthCalculationMemory(
                elastic_buckling_stress=8339.815719 * megapascal,
                critical_stress=348.7311926 * megapascal,
                nominal_strength=997371.211 * newton,
                design_strength=597228.27 * newton,
            ),
        ),
    ],
)
def test_w_section_flexural_buckling_major_axis_calc_memory_2016(
    section: DoublySymmetricI,
    beam_compression_param: BeamCompressionParam,
    design_type: DesignType,
    expected_flexural_buckling_calc_memory: BucklingStrengthCalculationMemory,
):
    beam = asdict(beam_compression_param)
    calc_memory = (
        section.compression(**beam, design_type=design_type)
        .criteria[StrengthType.FLEXURAL_BUCKLING_MAJOR_AXIS]
        .calculation_memory
    )
    assert simplify_dataclass(calc_memory) == approx(
        simplify_dataclass(expected_flexural_buckling_calc_memory)
    )


@mark.parametrize(
    "section, beam_compression_param, design_type, expected_flexural_buckling_calc_memory",
    [
        (
            create_aisc_section("W6X15", steel355MPa, ConstructionType.ROLLED),
            BeamCompressionParam(length_major_axis=1 * meter),
            DesignType.ASD,
            BucklingStrengthCalculationMemory(
                elastic_buckling_stress=2673.162613 * megapascal,
                critical_stress=335.8060215 * megapascal,
                nominal_strength=960405.2214 * newton,
                design_strength=575092.947 * newton,
            ),
        ),
    ],
)
def test_w_section_flexural_buckling_minor_axis_calc_memory_2016(
    section: DoublySymmetricI,
    beam_compression_param: BeamCompressionParam,
    design_type: DesignType,
    expected_flexural_buckling_calc_memory: BucklingStrengthCalculationMemory,
):
    beam = asdict(beam_compression_param)
    calc_memory = (
        section.compression(**beam, design_type=design_type)
        .criteria[StrengthType.FLEXURAL_BUCKLING_MINOR_AXIS]
        .calculation_memory
    )
    assert simplify_dataclass(calc_memory) == approx(
        simplify_dataclass(expected_flexural_buckling_calc_memory)
    )


@mark.parametrize(
    "section, beam_compression_param, design_type, expected_torsional_buckling_calc_memory",
    [
        (
            create_aisc_section("W6X15", steel355MPa, ConstructionType.ROLLED),
            BeamCompressionParam(length_major_axis=1 * meter),
            DesignType.ASD,
            BucklingStrengthCalculationMemory(
                elastic_buckling_stress=2734.629415 * megapascal,
                critical_stress=336.2258313 * megapascal,
                nominal_strength=961605.8776 * newton,
                design_strength=575811.9028 * newton,
            ),
        ),
    ],
)
def test_w_section_torsional_calc_memory_2016(
    section: DoublySymmetricI,
    beam_compression_param: BeamCompressionParam,
    design_type: DesignType,
    expected_torsional_buckling_calc_memory: BucklingStrengthCalculationMemory,
):
    beam = asdict(beam_compression_param)
    calc_memory = (
        section.compression(**beam, design_type=design_type)
        .criteria[StrengthType.TORSIONAL_BUCKLING]
        .calculation_memory
    )
    assert simplify_dataclass(calc_memory) == approx(
        simplify_dataclass(expected_torsional_buckling_calc_memory)
    )
