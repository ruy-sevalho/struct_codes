from dataclasses import dataclass

from struct_codes.definitions import ConstructionType, Section_2016, SectionType
from struct_codes.materials import Material
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


# class AISC_Section:
#     """
#     Type	Shape type: W, M, S, HP, C, MC, L, WT, MT, ST, 2L, HSS, PIPE
#     EDI_ STD_ Nomenclature	The shape designation according to the AISC Naming Convention for Structural Steel Products
#     AISC_  Manual_ Label	"The shape designation as seen in the AISC Steel Construction Manual, 15th Edition.  The exception to this is the designation for double angles. There is a separate listing (row) for each back-to-back spacing and configuration. Therefore, the shape designation reflects these two variables. The listings for double angles follow the convention specified in the AISC Naming Convention for Structural Steel Products for Use in Electronic Data Interchange (EDI), June 25, 2001."
#     T_F	"Boolean variable. A true, T, value indicates that there is a special note for that shape (see below). A false, F, value indicates that there are no special notes for that shape.

#     Special notes:
#     W-shapes: a value of T for: tf > 2 in.
#     M-shapes: a value of T indicates that the shape has sloped flanges.
#     WT-shapes: a value of T for: tf > 2 in
#     MT-shapes: a value of T indicates that the shape has sloped flanges.
#     W	Nominal weight, lb/ft (kg/m)
#     A	Cross-sectional area, in.2 (mm2)
#     d	Overall depth of member, or width of shorter leg for angles, or width of the outstanding legs of long legs back-to-back double angles, or the width of the back-to-back legs of short legs back-to-back double angles, in. (mm)
#     ddet	Detailing value of member depth, in. (mm)
#     Ht	Overall depth of square or rectangular HSS, in. (mm)
#     h	Depth of the flat wall of square or rectangular HSS, in. (mm)
#     OD	Outside diameter of round HSS or pipe, in. (mm)
#     bf	Flange width, in. (mm)
#     bfdet	Detailing value of flange width, in. (mm)
#     B	Overall width of square or rectangular HSS, in. (mm)
#     b	Width of the flat wall of square or rectangular HSS, or width of the longer leg for angles, or width of the back-to-back legs of long legs back-to-back double angles, or width of the outstanding legs of short legs back-to-back double angles, in. (mm)
#     ID	Inside diameter of round HSS or pipe, in. (mm)
#     tw	Web thickness, in. (mm)
#     twdet	Detailing value of web thickness, in. (mm)
#     twdet/2	Detailing value of tw/2, in. (mm)
#     tf	Flange thickness, in. (mm)
#     tfdet	Detailing value of flange thickness, in. (mm)
#     t	Thickness of angle leg, in. (mm)
#     tnom	HSS and pipe nominal wall thickness, in. (mm)
#     tdes	HSS and pipe design wall thickness, in. (mm)
#     kdes	Design distance from outer face of flange to web toe of fillet, in. (mm)
#     kdet	Detailing distance from outer face of flange to web toe of fillet, in. (mm)
#     k1	Detailing distance from center of web to flange toe of fillet, in. (mm)
#     x	Horizontal distance from designated member edge, as defined in the AISC Steel Construction Manual, to member centroidal axis, in. (mm)
#     y	Vertical distance from designated member edge, as defined in the AISC Steel Construction Manual, to member centroidal axis, in. (mm)
#     eo	Horizontal distance from designated member edge, as defined in the AISC Steel Construction Manual, to member shear center, in. (mm)
#     xp	Horizontal distance from designated member edge, as defined in the AISC Steel Construction Manual, to member plastic neutral axis, in. (mm)
#     yp	Vertical distance from designated member edge, as defined in the AISC Steel Construction Manual, to member plastic neutral axis, in. (mm)
#     bf/2tf	Slenderness ratio
#     b/t	Slenderness ratio for angles
#     b/tdes	Slenderness ratio for square or rectangular HSS
#     h/tw	Slenderness ratio
#     h/tdes	Slenderness ratio for square or rectangular HSS
#     D/t	Slenderness ratio for round HSS and pipe, or tee shapes
#     Ix	Moment of inertia about the x-axis, in.4 (mm4 /106)
#     Zx	Plastic section modulus about the x-axis, in.3 (mm3 /103)
#     Sx	Elastic section modulus about the x-axis, in.3 (mm3 /103)
#     rx	Radius of gyration about the x-axis, in. (mm)
#     Iy	Moment of inertia about the y-axis, in.4 (mm4 /106)
#     Zy	Plastic section modulus about the y-axis, in.3 (mm3 /103)
#     Sy	Elastic section modulus about the y-axis, in.3 (mm3 /103)
#     ry	Radius of gyration about the y-axis (with no separation for double angles back-to-back), in. (mm)
#     Iz	Moment of inertia about the z-axis, in.4 (mm4 /106)
#     rz	Radius of gyration about the z-axis, in. (mm)
#     Sz	Elastic section modulus about the z-axis, in.3 (mm3 /103)
#     J	Torsional moment of inertia, in.4 (mm4 /103)
#     Cw	Warping constant, in.6 (mm6 /109)
#     C	HSS torsional constant, in.3 (mm3 /103)
#     Wno	Normalized warping function, as used in Design Guide 9, in.2 (mm2)
#     Sw1	Warping statical moment at point 1 on cross section, as used in AISC Design Guide 9 and shown in Figures 1 and 2, in.4 (mm4 /106)
#     Sw2	Warping statical moment at point 2 on cross section, as used in AISC Design Guide 9 and shown in Figure 2, in.4 (mm4 /106)
#     Sw3	Warping statical moment at point 3 on cross section, as used in AISC Design Guide 9 and shown in Figure 2, in.4 (mm4 /106)
#     Qf	Statical moment for a point in the flange directly above the vertical edge of the web, as used in AISC Design Guide 9, in.3 (mm3 /103)
#     Qw	Statical moment for a point at mid-depth of the cross section, as used in AISC Design Guide 9, in.3 (mm3 /103)
#     ro	Polar radius of gyration about the shear center, in. (mm)
#     H	Flexural constant
#     tan(α)	Tangent of the angle between the y-y and z-z axes for single angles, where a is shown in Figure 3
#     Iw	Moment of inertia about the w-axis for single angles, in.4 (mm4 /106)
#     zA	Distance from point A to center of gravity along z-axis, as shown in Figure 3, in. (mm)
#     zB	Distance from point B to center of gravity along z-axis, as shown in Figure 3, in. (mm)
#     zC	Distance from point C to center of gravity along z-axis, as shown in Figure 3, in. (mm)
#     wA	Distance from point A to center of gravity along w-axis, as shown in Figure 3, in. (mm)
#     wB	Distance from point B to center of gravity along w-axis, as shown in Figure 3, in. (mm)
#     wC	Distance from point C to center of gravity along w-axis, as shown in Figure 3, in. (mm)
#     SwA	Elastic section modulus about the w-axis at point A on cross section, as shown in Figure 3, in.3 (mm3 /103)
#     SwB	Elastic section modulus about the w-axis at point B on cross section, as shown in Figure 3, in.3 (mm3 /103)
#     SwC	Elastic section modulus about the w-axis at point C on cross section, as shown in Figure 3, in.3 (mm3 /103)
#     SzA	Elastic section modulus about the z-axis at point A on cross section, as shown in Figure 3, in.3 (mm3 /103)
#     SzB	Elastic section modulus about the z-axis at point B on cross section, as shown in Figure 3, in.3 (mm3 /103)
#     SzC	Elastic section modulus about the z-axis at point C on cross section, as shown in Figure 3, in.3 (mm3 /103)
#     rts	Effective radius of gyration, in. (mm)
#     ho	Distance between the flange centroids, in. (mm)
#     PA	Shape perimeter minus one flange surface (or short leg surface for a single angle), as used in Design Guide 19, in. (mm)
#     PA2	Single angle shape perimeter minus long leg surface, as used in AISC Design Guide 19, in. (mm)
#     PB	Shape perimeter, as used in AISC Design Guide 19, in. (mm)
#     PC	Box perimeter minus one flange surface, as used in Design Guide 19, in. (mm)
#     PD	Box perimeter, as used in AISC Design Guide 19, in. (mm)
#     T	Distance between web toes of fillets at top and bottom of web, in. (mm)
#     WGi	The workable gage for the inner fastener holes in the flange that provides for entering and tightening clearances and edge distance and spacing requirements. The actual size, combination, and orientation of fastener components should be compared with the geometry of the cross section to ensure compatibility. See AISC Manual Part 1 for additional information, in. (mm)
#     WGo	The bolt spacing between inner and outer fastener holes when the workable gage is compatible with four holes across the flange. See AISC Manual Part 1 for additional information, in. (mm)
#     """

#     EDI_STD_Nomenclature_imp: str
#     AISC_Manual_Label_imp: str
#     EDI_STD_Nomenclature_metric: str
#     AISC_Manual_Label_metric: str
#     type: SectionType
#     T_F: Quantity
#     W: Quantity
#     A: Quantity
#     d: Quantity
#     ddet: Quantity
#     Ht: Quantity
#     h: Quantity
#     OD: Quantity
#     bf: Quantity
#     bfdet: Quantity
#     B: Quantity
#     b: Quantity
#     ID: Quantity
#     tw: Quantity
#     twdet: Quantity
#     twdet_2: Quantity
#     tf: Quantity
#     tfdet: Quantity
#     t: Quantity
#     tnom: Quantity
#     tdes: Quantity
#     kdes: Quantity
#     kdet: Quantity
#     k1: Quantity
#     x: Quantity
#     y: Quantity
#     eo: Quantity
#     xp: Quantity
#     yp: Quantity
#     bf_2tf: float
#     b_t: float
#     b_tdes: float
#     h_tw: float
#     h_tdes: float
#     D_t: float
#     Ix: Quantity
#     Zx: Quantity
#     Sx: Quantity
#     rx: Quantity
#     Iy: Quantity
#     Zy: Quantity
#     Sy: Quantity
#     ry: Quantity
#     Iz: Quantity
#     rz: Quantity
#     Sz: Quantity
#     J: Quantity
#     Cw: Quantity
#     C: Quantity
#     Wno: Quantity
#     Sw1: Quantity
#     Sw2: Quantity
#     Sw3: Quantity
#     Qf: Quantity
#     Qw: Quantity
#     ro: Quantity
#     H: float
#     tan_alpha: float
#     Iw: Quantity
#     zA: Quantity
#     zB: Quantity
#     zC: Quantity
#     wA: Quantity
#     wB: Quantity
#     wC: Quantity
#     SwA: Quantity
#     SwB: Quantity
#     SwC: Quantity
#     SzA: Quantity
#     SzB: Quantity
#     SzC: Quantity
#     rts: Quantity
#     ho: Quantity
#     PA: Quantity
#     PA2: Quantity
#     PB: Quantity
#     PC: Quantity
#     PD: Quantity
#     T: Quantity
#     WGi: Quantity
#     WGo: Quantity


@dataclass
class DoublySymmetricSlenderness:
    web_axial: Slenderness
    web_flexure_major_axis: Slenderness
    flange_axial: Slenderness
    flange_flexure_major_axis: Slenderness
    flange_flexure_minor_axis: Slenderness


@dataclass
class DoublySymmetricSlendernessCalcMemory:
    web_ratio: float
    flange_ratio: float
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
            web_ratio=self.web_ratio,
            flange_ratio=self.flange_ratio,
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
class DoublySymmetricI:
    geometry: DoublySymmetricIGeo
    material: Material
    construction: ConstructionType

    @property
    def kc_coeficient(self):
        return kc_coefficient(heigth_to_thickness_ratio=self.geometry.h_tw)

    @property
    def _axial_flange_built_up_limit_ratio(self) -> float:
        return axial_built_up_flanges_limit_ratio(
            modulus_linear=self.material.modulus_linear,
            yield_strength=self.material.yield_strength,
            kc_coefficient=self.kc_coeficient,
        )

    @property
    def _axial_flange_rolled_limit_ratio(self) -> float:
        return axial_rolled_flanges_limit_ratio(
            modulus_linear=self.material.modulus_linear,
            yield_strength=self.material.yield_strength,
        )

    @property
    def _axial_flange_limit_ratio(self) -> float:
        table = {
            ConstructionType.BUILT_UP: self._axial_flange_built_up_limit_ratio,
            ConstructionType.ROLLED: self._axial_flange_rolled_limit_ratio,
        }
        return table[self.construction]

    @property
    def _axial_web_limit_ratio(self) -> float:
        return axial_doubly_symmetric_web_limit(
            modulus_linear=self.material.modulus_linear,
            yield_strength=self.material.yield_strength,
        )

    @property
    def _flexural_flange_rolled_compact_limit_ratio(self) -> float:
        return flexural_rolled_i_channel_tees_flange_compact_limit(
            modulus_linear=self.material.modulus_linear,
            yield_strength=self.material.yield_strength,
        )

    @property
    def _flexural_flange_rolled_slender_limit_ratio(self) -> float:
        return flexural_rolled_i_channel_tees_flange_slender_limit(
            modulus_linear=self.material.modulus_linear,
            yield_strength=self.material.yield_strength,
        )

    @property
    def _flexural_flange_built_up_compact_limit_ratio(self) -> float:
        return flexural_built_up_i_flange_compact_limit(
            modulus_linear=self.material.modulus_linear,
            yield_strength=self.material.yield_strength,
        )

    @property
    def _flexural_flange_built_up_slender_limit_ratio(self) -> float:
        return flexural_built_up_i_flange_slender_limit(
            modulus_linear=self.material.modulus_linear,
            yield_strength=self.material.yield_strength,
            kc_coefficient=self.kc_coeficient,
        )

    @property
    def _flexural_flange_compact_limit(self) -> Slenderness:
        table = {
            ConstructionType.ROLLED: self._flexural_flange_rolled_compact_limit_ratio,
            ConstructionType.BUILT_UP: self._flexural_flange_built_up_compact_limit_ratio,
        }
        return table[self.construction]

    @property
    def _flexural_flange_slender_limit(self) -> Slenderness:
        table = {
            ConstructionType.ROLLED: self._flexural_flange_rolled_slender_limit_ratio,
            ConstructionType.BUILT_UP: self._flexural_flange_built_up_slender_limit_ratio,
        }
        return table[self.construction]

    @property
    def _flexural_web_slender_limit(self) -> Slenderness:
        return flexural_doubly_symmetric_web_slender_limit_ratio(
            modulus_linear=self.material.modulus_linear,
            yield_strength=self.material.modulus_linear,
        )

    @property
    def flexural_flange_slender_limit_ratio(self) -> float:
        table = {
            ConstructionType.BUILT_UP: self._flexural_flange_built_up_slender_limit_ratio,
            ConstructionType.ROLLED: self._flexural_flange_rolled_slender_limit_ratio,
        }
        return table[self.construction]

    @property
    def _flexural_web_compact_limit(self) -> Slenderness:
        return flexural_doubly_symmetric_web_compact_limit(
            modulus_linear=self.material.modulus_linear,
            yield_strength=self.material.modulus_linear,
        )

    @property
    def _flexural_web_major_axis_slenderness(self) -> Slenderness:
        return flexural_slenderness_per_element(
            limit_slender=self._flexural_web_slender_limit
        )

    @property
    def slenderness_2016(self) -> DoublySymmetricSlenderness:
        return self._slenderness_2016.slenderness

    @property
    def slenderness_2016_calc_memory(self) -> DoublySymmetricSlendernessCalcMemory:
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
