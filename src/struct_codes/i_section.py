from dataclasses import dataclass

from struct_codes._compression import FlexuralBucklingStrengthCalculation
from struct_codes._tension import TensionCalculation2016, TensionCalculationMemory
from struct_codes.criteria import DesignType
from struct_codes.materials import Material
from struct_codes.sections import (
    CalculationCollection,
    Connection,
    ConstructionType,
    Section,
    SectionType,
)
from struct_codes.slenderness import (
    AxialSlendernessCalcMemory,
    FlexuralSlendernessCalcMemory,
    Slenderness,
    axial_built_up_flanges_limit_ratio,
    axial_doubly_symmetric_web_limit,
    axial_rolled_flanges_limit_ratio,
    axial_slenderness_per_element,
    flexural_built_up_i_flange_compact_limit,
    flexural_built_up_i_flange_slender_limit,
    flexural_doubly_symmetric_web_compact_limit,
    flexural_doubly_symmetric_web_slender_limit_ratio,
    flexural_rolled_i_channel_tees_flange_compact_limit,
    flexural_rolled_i_channel_tees_flange_slender_limit,
    flexural_slenderness_per_element,
    kc_coefficient,
)
from struct_codes.units import Quantity, millimeter


@dataclass
class DoublySymmetricIGeo:
    EDI_STD_Nomenclature_imp: str
    AISC_Manual_Label_imp: str
    EDI_STD_Nomenclature_metric: str
    AISC_Manual_Label_metric: str
    type: SectionType
    T_F: Quantity
    W: Quantity
    A: Quantity
    d: Quantity
    ddet: Quantity
    bf: Quantity
    bfdet: Quantity
    tw: Quantity
    twdet: Quantity
    twdet_2: Quantity
    tf: Quantity
    tfdet: Quantity
    kdes: Quantity
    kdet: Quantity
    k1: Quantity
    bf_2tf: float
    h_tw: float
    Ix: Quantity
    Zx: Quantity
    Sx: Quantity
    rx: Quantity
    Iy: Quantity
    Zy: Quantity
    Sy: Quantity
    ry: Quantity
    J: Quantity
    Cw: Quantity
    Wno: Quantity
    Sw1: Quantity
    Qf: Quantity
    Qw: Quantity
    rts: Quantity
    ho: Quantity
    PA: Quantity
    PB: Quantity
    PC: Quantity
    PD: Quantity
    T: Quantity
    WGi: Quantity
    WGo: Quantity


@dataclass
class DoublySymmetricSlenderness:
    web_axial: Slenderness
    web_flexure_major_axis: Slenderness
    flange_axial: Slenderness
    flange_flexure_major_axis: Slenderness
    flange_flexure_minor_axis: Slenderness


@dataclass
class DoublySymmetricSlendernessCalcMemory:
    web_axial_slender_limit: float
    web_axial_slenderness: Slenderness
    web_flexural_compact_limit: float
    web_flexural_slender_limit: float
    web_flexural_slenderness: Slenderness
    flange_axial_slender_limit: float
    flange_axial_slenderness: Slenderness
    flange_flexural_major_axis_compact_limit: float
    flange_flexural_major_axis_slender_limit: float
    flange_flexural_major_axis_slenderness: Slenderness
    flange_flexural_minor_axis_compact_limit: float
    flange_flexural_minor_axis_slender_limit: float
    flange_flexural_minor_axis_slenderness: Slenderness


@dataclass
class DoublySymmetricSlendernessCalculation2016:
    construction: ConstructionType
    web_ratio: float
    flange_ratio: float
    modulus_linear: Quantity
    yield_strength: Quantity

    @property
    def kc_coeficient(self):
        return kc_coefficient(heigth_to_thickness_ratio=self.web_ratio)

    @property
    def _flange_axial_built_up_limit_ratio(self) -> float:
        return axial_built_up_flanges_limit_ratio(
            modulus_linear=self.modulus_linear,
            yield_strength=self.yield_strength,
            kc_coefficient=self.kc_coeficient,
        )

    @property
    def _flange_axial_rolled_limit_ratio(self) -> float:
        return axial_rolled_flanges_limit_ratio(
            modulus_linear=self.modulus_linear,
            yield_strength=self.yield_strength,
        )

    @property
    def _flange_axial_limit(self) -> float:
        table = {
            ConstructionType.BUILT_UP: self._flange_axial_built_up_limit_ratio,
            ConstructionType.ROLLED: self._flange_axial_rolled_limit_ratio,
        }
        return table[self.construction]

    @property
    def _web_axial_slender_limit(self) -> float:
        return axial_doubly_symmetric_web_limit(
            modulus_linear=self.modulus_linear,
            yield_strength=self.yield_strength,
        )

    @property
    def _flange_flexural_rolled_compact_limit(self) -> float:
        return flexural_rolled_i_channel_tees_flange_compact_limit(
            modulus_linear=self.modulus_linear,
            yield_strength=self.yield_strength,
        )

    @property
    def _flange_flexural_rolled_slender_limit(self) -> float:
        return flexural_rolled_i_channel_tees_flange_slender_limit(
            modulus_linear=self.modulus_linear,
            yield_strength=self.yield_strength,
        )

    @property
    def _flange_flexural_built_up_compact_limit_ratio(self) -> float:
        return flexural_built_up_i_flange_compact_limit(
            modulus_linear=self.modulus_linear,
            yield_strength=self.yield_strength,
        )

    @property
    def _flange_flexural_built_up_slender_limit_ratio(self) -> float:
        return flexural_built_up_i_flange_slender_limit(
            modulus_linear=self.modulus_linear,
            yield_strength=self.yield_strength,
            kc_coefficient=self.kc_coeficient,
        )

    @property
    def _flange_flexural_compact_limit(self) -> Slenderness:
        table = {
            ConstructionType.ROLLED: self._flange_flexural_rolled_compact_limit,
            ConstructionType.BUILT_UP: self._flange_flexural_built_up_compact_limit_ratio,
        }
        return table[self.construction]

    @property
    def _flange_flexural_slender_limit(self) -> Slenderness:
        table = {
            ConstructionType.ROLLED: self._flange_flexural_rolled_slender_limit,
            ConstructionType.BUILT_UP: self._flange_flexural_built_up_slender_limit_ratio,
        }
        return table[self.construction]

    @property
    def _web_flexural_slender_limit(self) -> Slenderness:
        return flexural_doubly_symmetric_web_slender_limit_ratio(
            modulus_linear=self.modulus_linear,
            yield_strength=self.yield_strength,
        )

    @property
    def _flange_flexural_slender_limit(self) -> float:
        table = {
            ConstructionType.BUILT_UP: self._flange_flexural_built_up_slender_limit_ratio,
            ConstructionType.ROLLED: self._flange_flexural_rolled_slender_limit,
        }
        return table[self.construction]

    @property
    def _web_flexural_compact_limit(self) -> Slenderness:
        return flexural_doubly_symmetric_web_compact_limit(
            modulus_linear=self.modulus_linear,
            yield_strength=self.yield_strength,
        )

    @property
    def _web_axial_slenderness(self) -> Slenderness:
        return axial_slenderness_per_element(
            ratio=self.web_ratio, limit=self._web_axial_slender_limit
        )

    @property
    def _web_flexural_slenderness(self) -> Slenderness:
        return flexural_slenderness_per_element(
            limit_slender=self._web_flexural_slender_limit,
            limit_compact=self._web_flexural_compact_limit,
            ratio=self.web_ratio,
        )

    @property
    def _flange_axial_slenderness(self) -> Slenderness:
        return axial_slenderness_per_element(
            ratio=self.flange_ratio, limit=self._flange_axial_limit
        )

    @property
    def _flange_flexural_major_axis_slenderness(self) -> Slenderness:
        return flexural_slenderness_per_element(
            limit_slender=self._flange_flexural_slender_limit,
            limit_compact=self._flange_flexural_compact_limit,
            ratio=self.flange_ratio,
        )

    @property
    def _flange_flexural_minor_axis_slenderness(self) -> Slenderness:
        return flexural_slenderness_per_element(
            limit_slender=self._flange_flexural_rolled_slender_limit,
            limit_compact=self._flange_flexural_rolled_compact_limit,
            ratio=self.flange_ratio,
        )

    @property
    def slenderness(self) -> DoublySymmetricSlenderness:
        return DoublySymmetricSlenderness(
            web_axial=self._web_axial_slenderness,
            web_flexure_major_axis=self._web_flexural_slenderness,
            flange_axial=self._flange_axial_slenderness,
            flange_flexure_major_axis=self._flange_flexural_major_axis_slenderness,
            flange_flexure_minor_axis=self._flange_flexural_minor_axis_slenderness,
        )

    @property
    def calc_memory(self) -> DoublySymmetricSlendernessCalcMemory:
        return DoublySymmetricSlendernessCalcMemory(
            web_axial_slender_limit=self._web_axial_slender_limit,
            web_axial_slenderness=self._web_axial_slenderness,
            web_flexural_slender_limit=self._web_flexural_slender_limit,
            web_flexural_compact_limit=self._web_flexural_compact_limit,
            web_flexural_slenderness=self._web_flexural_slenderness,
            flange_axial_slender_limit=self._flange_axial_limit,
            flange_axial_slenderness=self._flange_axial_slenderness,
            flange_flexural_major_axis_compact_limit=self._flange_flexural_compact_limit,
            flange_flexural_major_axis_slender_limit=self._flange_flexural_slender_limit,
            flange_flexural_major_axis_slenderness=self._flange_flexural_major_axis_slenderness,
            flange_flexural_minor_axis_compact_limit=self._flange_flexural_rolled_compact_limit,
            flange_flexural_minor_axis_slender_limit=self._flange_flexural_rolled_slender_limit,
            flange_flexural_minor_axis_slenderness=self._flange_flexural_minor_axis_slenderness,
        )


@dataclass
class CompressionCalculation(CalculationCollection):
    flexural_buckling_major_axis: FlexuralBucklingStrengthCalculation = None
    flexural_buckling_minor_axis: FlexuralBucklingStrengthCalculation = None
    torsional_buckling: FlexuralBucklingStrengthCalculation = None


@dataclass
class DoublySymmetricI:
    geometry: DoublySymmetricIGeo
    material: Material
    construction: ConstructionType = ConstructionType.ROLLED
    connection: Connection | None = None

    def compression(
        self,
        length_major_axis: Quantity,
        factor_k_major_axis: float = 1.0,
        length_minor_axis: Quantity = None,
        factor_k_minor_axis: float = 1.0,
        length_torsion: Quantity = None,
        factor_k_torsion: float = 1.0,
        design_type: DesignType = DesignType.ASD,
        required_strength: Quantity | None = None,
    ):
        return CompressionCalculation(
            flexural_buckling_major_axis=FlexuralBucklingStrengthCalculation(
                length=length_major_axis,
                factor_k=factor_k_major_axis,
                yield_stress=self.material.yield_strength,
                modulus_linear=self.material.modulus_linear,
                gross_area=self.geometry.A,
                radius_of_gyration=self.geometry.rx,
                design_type=design_type,
            ),
            flexural_buckling_minor_axis=None,
            torsional_buckling=None,
        )

    @property
    def slenderness_2016(self) -> DoublySymmetricSlenderness:
        return self._slenderness_2016.slenderness

    @property
    def slenderness_calc_memory_2016(self) -> DoublySymmetricSlendernessCalcMemory:
        return self._slenderness_2016.calc_memory

    @property
    def _slenderness_2016(self) -> DoublySymmetricSlendernessCalculation2016:
        return DoublySymmetricSlendernessCalculation2016(
            construction=self.construction,
            web_ratio=self.geometry.h_tw,
            flange_ratio=self.geometry.bf_2tf,
            modulus_linear=self.material.modulus_linear,
            yield_strength=self.material.yield_strength,
        )

    @property
    def _net_area(self) -> Quantity:
        reduction = 0
        if self.connection:
            reduction = self.connection.area_reduction
        return self.geometry.A - reduction

    def _tension_calculation_2016(self, design_type: DesignType):
        return TensionCalculation2016(
            net_area=self._net_area,
            gross_area=self.geometry.A,
            yield_stress=self.material.yield_strength,
            ultimate_stress=self.material.ultimate_strength,
            design_type=design_type,
        )

    def tension_calc_memory_2016(
        self, design_type: DesignType = DesignType.ASD
    ) -> TensionCalculationMemory:
        return self._tension_calculation_2016(
            design_type=design_type
        ).calculation_memory

    def tension(
        self, design_type: DesignType = DesignType.ASD
    ) -> TensionCalculation2016:
        return self._tension_calculation_2016(design_type=design_type)
