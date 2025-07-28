from pytest import mark
from unit_processing import compare_quantites

from struct_codes.aisc_database import AISC_SECTIONS_15ED, get_aisc_section_geo_and_type
from struct_codes.analysis import Analysis
from struct_codes.beam import Beam
from struct_codes.criteria import DesignType, StrengthType
from struct_codes.materials import Material, steel355MPa
from struct_codes.sections import (
    ConstructionType,
    SectionClassification,
    SectionGeometry,
)
from struct_codes.units import Quantity, meter, newton


@mark.parametrize(
    """
    section_geo, 
    section_type, 
    material, 
    construction, 
    beam,
    design_type, 
    expected_design_strength
    """,
    [
        (
            *get_aisc_section_geo_and_type("W6X15"),
            steel355MPa,
            ConstructionType.ROLLED,
            Beam(1 * meter),
            DesignType.ASD,
            597228.27 * newton,
        ),
    ],
)
def test_flexural_buckling_major_axis_15ed(
    section_geo: SectionGeometry,
    section_type: SectionClassification,
    material: Material,
    construction: ConstructionType,
    beam: Beam,
    design_type: DesignType,
    expected_design_strength: Quantity,
):
    analysis = Analysis(
        geometry=section_geo,
        section_type=section_type,
        material=material,
        construction=construction,
        beam=beam,
        design_type=design_type,
    )

    ds = analysis.compression.criteria[
        StrengthType.FLEXURAL_BUCKLING_MAJOR_AXIS
    ].design_strength
    compare_quantites(ds, expected_design_strength)
