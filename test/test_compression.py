from dataclasses import asdict
from typing import Any

from pint import Quantity
from pytest import approx, mark
from unit_processing import simplify_dataclass, simplify_units

from struct_codes._compression import (
    BeamCompressionParam,
    FlexuralBucklingStrengthCalculationMemory,
)
from struct_codes.aisc_database import create_aisc_section
from struct_codes.criteria import DesignType
from struct_codes.i_section import DoublySymmetricI
from struct_codes.materials import steel355MPa
from struct_codes.sections import ConstructionType, Section
from struct_codes.units import kilonewton, megapascal, meter, newton


@mark.parametrize(
    "section, beam_compression_param, design_type, expected_flexural_buckling_calc_memory",
    [
        (
            create_aisc_section("W6X15", steel355MPa, ConstructionType.ROLLED),
            BeamCompressionParam(length_major_axis=1 * meter),
            DesignType.ASD,
            FlexuralBucklingStrengthCalculationMemory(
                beam_slenderness=15.38461538,
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
    expected_flexural_buckling_calc_memory,
):
    beam = asdict(beam_compression_param)
    calc_memory = section.compression(
        **beam, design_type=design_type
    ).flexural_buckling_major_axis.calculation_memory
    assert simplify_dataclass(calc_memory) == approx(
        simplify_dataclass(expected_flexural_buckling_calc_memory)
    )
