from dataclasses import dataclass

from struct_codes.criteria import DesignType, StrengthType
from struct_codes.i_section._compression import (
    BucklingStrengthCalculationMixin,
    FlexuralBucklingStrengthCalculation,
    TorsionalBucklingDoublySymmetricStrengthCalculation,
)
from struct_codes.i_section._flexure import (
    LateralTorsionalBucklingCalculation2016,
    MinorAxisYieldingCalculation2016,
    YieldingMomentCalculation16,
)
from struct_codes.i_section._shear import WebShearCalculation2016
from struct_codes.i_section._slenderness import (
    DoublySymmetricSlenderness,
    DoublySymmetricSlendernessCalcMemory,
    DoublySymmetricSlendernessCalculation2016,
    _is_slender,
)
from struct_codes.i_section._tension import (
    TensionCalculation2016,
    TesionUltimateCalculation,
    TesionYieldCalculation,
)
from struct_codes.materials import Material
from struct_codes.sections import (
    Connection,
    ConstructionType,
    LoadStrengthCalculation,
    SectionType,
)
from struct_codes.units import Quantity


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
        compression = LoadStrengthCalculation(
            criteria={
                StrengthType.FLEXURAL_BUCKLING_MAJOR_AXIS: FlexuralBucklingStrengthCalculation(
                    length=length_major_axis,
                    factor_k=factor_k_major_axis,
                    yield_stress=self.material.yield_strength,
                    modulus_linear=self.material.modulus_linear,
                    gross_area=self.geometry.A,
                    radius_of_gyration=self.geometry.rx,
                    design_type=design_type,
                ),
                StrengthType.FLEXURAL_BUCKLING_MINOR_AXIS: FlexuralBucklingStrengthCalculation(
                    length=length_minor_axis or length_major_axis,
                    factor_k=factor_k_minor_axis or factor_k_major_axis,
                    yield_stress=self.material.yield_strength,
                    modulus_linear=self.material.modulus_linear,
                    gross_area=self.geometry.A,
                    radius_of_gyration=self.geometry.ry,
                    design_type=design_type,
                ),
                StrengthType.TORSIONAL_BUCKLING: TorsionalBucklingDoublySymmetricStrengthCalculation(
                    design_type=design_type,
                    yield_stress=self.material.yield_strength,
                    gross_area=self.geometry.A,
                    length=length_torsion or length_major_axis,
                    factor_k=factor_k_torsion or factor_k_major_axis,
                    modulus_linear=self.material.modulus_linear,
                    modulus_shear=self.material.modulus_shear,
                    major_axis_inertia=self.geometry.Ix,
                    minor_axis_inertia=self.geometry.Iy,
                    torsional_constant=self.geometry.J,
                    warping_constant=self.geometry.Cw,
                ),
            }
        )
        # TODO implement cases for section with slender elements
        design_calculation: BucklingStrengthCalculationMixin = (
            compression.design_strength_calculation
        )
        _is_slender(
            lamdba_ratio=self._slenderness_2016.flange_ratio,
            lambda_limit=self._slenderness_2016._flange_axial_limit,
            yield_stess=self.material.yield_strength,
            critical_stress=design_calculation.critical_stress,
        )
        _is_slender(
            lamdba_ratio=self._slenderness_2016.web_ratio,
            lambda_limit=self._slenderness_2016._web_axial_slender_limit,
            yield_stess=self.material.yield_strength,
            critical_stress=design_calculation.critical_stress,
        )
        return compression

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

    def _tension_2016(self, design_type: DesignType):
        shear_lag_factor = 1.0
        if self.connection:
            shear_lag_factor = self.connection.shear_lag_factor
        return LoadStrengthCalculation(
            criteria={
                StrengthType.YIELD: TesionYieldCalculation(
                    gross_area=self.geometry.A,
                    yield_stress=self.material.yield_strength,
                    design_type=design_type,
                ),
                StrengthType.ULTIMATE: TesionUltimateCalculation(
                    net_area=self._net_area,
                    ultimate_stress=self.material.ultimate_strength,
                    shear_lag_factor=shear_lag_factor,
                    design_type=design_type,
                ),
            }
        )

    def tension(
        self, design_type: DesignType = DesignType.ASD
    ) -> LoadStrengthCalculation:
        return self._tension_2016(design_type=design_type)

    def flexure_major_axis(
        self,
        length: Quantity = None,
        lateral_torsional_buckling_modification_factor: float = 1.0,
        design_type: DesignType = DesignType.ASD,
    ) -> LoadStrengthCalculation:
        return LoadStrengthCalculation(
            criteria={
                StrengthType.YIELD: YieldingMomentCalculation16(
                    plastic_section_modulus=self.geometry.Zx,
                    yield_stress=self.material.yield_strength,
                    design_type=design_type,
                ),
                StrengthType.LATERAL_TORSIONAL_BUCKLING: LateralTorsionalBucklingCalculation2016(
                    length=length,
                    modulus=self.material.modulus_linear,
                    yield_stress=self.material.yield_strength,
                    plastic_section_modulus=self.geometry.Zx,
                    elastic_section_modulus=self.geometry.Sx,
                    distance_between_flange_centroids=self.geometry.ho,
                    torsional_constant=self.geometry.J,
                    warping_constant=self.geometry.Cw,
                    radius_of_gyration=self.geometry.ry,
                    minor_axis_inertia=self.geometry.Iy,
                    modification_factor=lateral_torsional_buckling_modification_factor,
                    coefficient_c=1,
                    design_type=design_type,
                ),
            }
        )

    def flexure_minor_axis(self, design_type: DesignType = DesignType.ASD):
        return LoadStrengthCalculation(
            {
                StrengthType.YIELD: MinorAxisYieldingCalculation2016(
                    yield_stress=self.material.yield_strength,
                    plastic_section_modulus=self.geometry.Zy,
                    elastic_section_modulus=self.geometry.Sy,
                    design_type=design_type,
                ),
            }
        )

    def shear_major_axis(self, design_type: DesignType = DesignType.ASD):
        return LoadStrengthCalculation(
            criteria={
                StrengthType.WEB_SHEAR: WebShearCalculation2016(
                    yield_stress=self.material.yield_strength,
                    web_area=self.geometry.d * self.geometry.tw,
                    modulus=self.material.modulus_linear,
                    web_ratio=self.geometry.h_tw,
                    construction_type=self.construction,
                    design_type=design_type,
                )
            }
        )
