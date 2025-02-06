from dataclasses import asdict

from pytest import approx, mark
from unit_processing import simplify_dataclass

from struct_codes.aisc_database import create_aisc_section
from struct_codes.criteria import DesignType
from struct_codes.definitions import ConstructionType, Section_2016
from struct_codes.i_section import (
    DoublySymmetricSlendernessCalcMemory,
    TensionCalculationMemory,
)
from struct_codes.materials import steel355MPa
from struct_codes.units import centemiter, kilonewton, megapascal, millimeter, newton


@mark.parametrize(
    "section, expected_tension_calc_memory",
    [
        (
            create_aisc_section("W6X15", steel355MPa, ConstructionType.ROLLED),
            TensionCalculationMemory(
                net_area=2860 * millimeter**2,
                gross_area=2860 * millimeter**2,
                net_effective_area=2860 * millimeter**2,
                shear_lag_factor=1.0,
                ultimate_stress=500 * megapascal,
                yield_stress=355 * megapascal,
                nominal_yielding_strength=1_015_300 * newton,
                nominal_ultimate_strength=1_430_000 * newton,
                ultimate_strength=715_000 * newton,
                yielding_strength=607_964.0719 * newton,
                design_strength=607_964.0719 * newton,
                design_type=DesignType.ASD,
            ),
        )
    ],
)
def test_tension_calc_memory(
    section: Section_2016,
    expected_tension_calc_memory: TensionCalculationMemory,
):
    tension_calc_memory = section.tension_calc_memory_2016()
    assert simplify_dataclass(tension_calc_memory) == approx(
        simplify_dataclass(expected_tension_calc_memory)
    )
