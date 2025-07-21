from unit_processing import compare_quantites

from struct_codes.aisc_database import AISC_SECTIONS_15ED
from struct_codes.analysis import Analysis
from struct_codes.criteria import DesignType
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
    length_major_axis,
    design_type, 
    expected_design_strength
    """,
    [
        (
            AISC_SECTIONS_15ED["W6X15"],
            AISC_SECTIONS_15ED["W6X15"]["type"],
            steel355MPa,
            ConstructionType.ROLLED,
            1 * meter,
            DesignType.ASD,
            597228.27 * newton,
        ),
    ],
)
def test_w_section_flexural_buckling_major_axis_calc_memory_2016(
    section_geo: SectionGeometry,
    section_type: SectionClassification,
    material: Material,
    construction: ConstructionType,
    length_major_axis: Quantity,
    design_type: DesignType,
    expected_design_strength: Quantity,
):
    analysis = Analysis(
        geometry=section_geo,
        section_type=section_type,
        material=material,
        construction=construction,
        length_major_axis=length_major_axis,
        design_type=design_type,
    )

    ds = (
        section.compression(**beam, design_type=design_type)
        .criteria[StrengthType.FLEXURAL_BUCKLING_MAJOR_AXIS]
        .design_strength
    )
    compare_quantites(ds, expected_design_strength)
