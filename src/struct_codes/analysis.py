from struct_codes.compression import FlexuralBucklingStrengthCalculation
from struct_codes.criteria import DesignType, StrengthType
from struct_codes.materials import Material
from struct_codes.sections import (
    CHANEL,
    DOUBLY_SYMMETRIC_I,
    Beam,
    ConstructionType,
    LoadStrengthCalculation,
    RuleEd,
    SectionClassification,
    SectionGeometry,
    SectionType,
    section_table
)
from struct_codes.slenderness import DefaultSlendernessCalculation2016
from struct_codes.units import Quantity


from dataclasses import dataclass


@dataclass
class BeamAnalysis:
    geometry: SectionGeometry
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
    def flexural_bucking_major_axis(self):
        if self.type in DOUBLY_SYMMETRIC_I + CHANEL:
            calculation = FlexuralBucklingStrengthCalculation(
                yield_stress=self.material.yield_strength,
                gross_area=self.geometry.A,
                length=self.beam.length_major_axis,
                factor_k=self.beam.factor_k_major_axis,
                radius_of_gyration=self.geometry.rx,
            )
        if self.type in 
            NotImplementedError(f"Flexural buckling not implemented for section {self.type.value}")
            

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
