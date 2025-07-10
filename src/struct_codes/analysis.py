from dataclasses import dataclass

from struct_codes.compression import (
    FlexuralBucklingStrengthCalculation,
    TorsionalBucklingDoublySymmetricStrengthCalculation,
)
from struct_codes.criteria import DesignType, StrengthType
from struct_codes.materials import Material
from struct_codes.sections import (
    ANGLE,
    CHANEL,
    DOUBLY_SYMMETRIC_I,
    HSS,
    PIPE,
    AiscSectionGeometry,
    ConstructionType,
    LoadStrengthCalculation,
    RuleEd,
    SectionClassification,
    SectionType,
    section_table,
)
from struct_codes.slenderness import DefaultSlendernessCalculation2016
from struct_codes.units import Quantity


@dataclass
class Beam:
    length_major_axis: Quantity
    factor_k_major_axis: float = 1.0
    length_minor_axis: Quantity = None
    factor_k_minor_axis: float = 1.0
    length_torsion: Quantity = None
    factor_k_torsion: float = 1.0
    length_bracing_lateral_torsional_buckling: Quantity = None


@dataclass
class BeamAnalysis:
    geometry: AiscSectionGeometry
    material: Material
    construction: ConstructionType
    beam: Beam
    design_type: DesignType = DesignType.ASD
    rule_ed: RuleEd = RuleEd.TWENTY_SIXTEEN

    @property
    def type(self) -> SectionType:
        return self.geometry["type"]

    @property
    def section_classification(self):
        return section_table[self.type]

    @property
    def flexural_bucking_minor_axis_compact_E3(self):
        return FlexuralBucklingStrengthCalculation(
            yield_stress=self.material.yield_strength,
            gross_area=self.geometry.A,
            length=self.beam.length_minor_axis or self.beam.length_major_axis,
            factor_k=self.beam.factor_k_major_axis or self.beam.factor_k_major_axis,
            radius_of_gyration=self.geometry.ry,
        )

    @property
    def flexural_bucking_major_axis_compact_E3(self):
        return FlexuralBucklingStrengthCalculation(
            yield_stress=self.material.yield_strength,
            gross_area=self.geometry.A,
            length=self.beam.length_major_axis,
            factor_k=self.beam.factor_k_major_axis,
            radius_of_gyration=self.geometry.rx,
        )

    @property
    def flexural_torsional_buckling_E4(self):
        table = {
            SectionClassification.DOUBLY_SYMMETRIC_I: TorsionalBucklingDoublySymmetricStrengthCalculation(
                yield_stress=self.material.yield_strength,
                gross_area=self.geometry.A,
                modulus_linear=self.material.modulus_linear,
                modulus_shear=self.material.modulus_shear,
                major_axis_inertia=self.geometry.Ix,
                minor_axis_inertia=self.geometry.Iy,
                torsional_constant=self.geometry.J,
                warping_constant=self.geometry.Cw,
            ),
        }
        return table[self.section_classification]

    def compression(self) -> LoadStrengthCalculation:
        criteria = {
            StrengthType.FLEXURAL_BUCKLING_MAJOR_AXIS: FlexuralBucklingStrengthCalculation(
                yield_stress=self.material.yield_strength,
                gross_area=self.geometry.A,
                length=self.beam.length_major_axis,
                factor_k=self.beam.factor_k_major_axis,
                radius_of_gyration=self.geometry.rx,
            )
        }
        return LoadStrengthCalculation(criteria=criteria)

    def flexure_major_axis_positive(
        self, modification_factor: float = 1.0
    ) -> LoadStrengthCalculation: ...

    def flexure_minor_axis(self) -> LoadStrengthCalculation: ...

    def shear_major_axis(self) -> LoadStrengthCalculation: ...

    def shear_minor_axis(self) -> LoadStrengthCalculation: ...

    def check_load(
        axial_force: Quantity = None,
        major_axis_bending_moment: Quantity = None,
        minor_axis_bending_moment: Quantity = None,
        major_axis_shear_force: Quantity = None,
        minor_axis_shear_force: Quantity = None,
        torsion: Quantity = None,
        major_axis_bending_modification_factor: float = 1,
    ):
        return

    @property
    def _slenderness_2016(self):
        return DefaultSlendernessCalculation2016(
            construction=self.construction,
            web_ratio=self.geometry.h_tw,
            flange_ratio=self.geometry.bf_2tf,
            modulus_linear=self.material.modulus_linear,
            yield_strength=self.material.yield_strength,
        )

    @property
    def slenderness(self):
        table = {RuleEd.TWENTY_SIXTEEN: self._slenderness_2016}
        return table[self.rule_ed]
