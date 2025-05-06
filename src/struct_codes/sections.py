from dataclasses import dataclass
from enum import Enum, StrEnum, auto
from typing import Protocol

from struct_codes.criteria import StrengthMixin, StrengthType
from struct_codes.units import Quantity


class RuleEd(str, Enum):
    TWENTY_SIXTEEN = "2016"


class SectionType(str, Enum):
    Two_L = ("2L",)
    C = "C"
    HP = "HP"
    HSS = "HSS"
    L = "L"
    M = "M"
    MC = "MC"
    MT = "MT"
    PIPE = "PIPE"
    S = "S"
    ST = "ST"
    W = "W"
    WT = "WT"


class SectionClassification(StrEnum):
    DOUBLY_SYMMETRIC_I = auto()
    SINGLY_SYMMETRIC_I = auto()
    CHANEL = auto()
    TEE = auto()
    TWO_L = auto()
    ANGLE = auto()
    HSS = auto()
    PIPE = auto()


section_table = {
    SectionType.C: SectionClassification.CHANEL,
    SectionType.HP: SectionClassification.DOUBLY_SYMMETRIC_I,
    SectionType.HSS: SectionClassification.HSS,
    SectionType.L: SectionClassification.ANGLE,
    SectionType.M: SectionClassification.DOUBLY_SYMMETRIC_I,
    SectionType.MC: SectionClassification.CHANEL,
    SectionType.MT: SectionClassification.TEE,
    SectionType.PIPE: SectionClassification.PIPE,
    SectionType.S: SectionClassification.DOUBLY_SYMMETRIC_I,
    SectionType.ST: SectionClassification.TEE,
    SectionType.Two_L: SectionClassification.TWO_L,
    SectionType.W: SectionClassification.DOUBLY_SYMMETRIC_I,
}

DOUBLY_SYMMETRIC_I = (SectionType.W, SectionType.WT, SectionType.M, SectionType.HP)
CHANEL = (
    SectionType.C,
    SectionType.MC,
)
ANGLE = (SectionType.L,)
TEE = (SectionType.Two_L, SectionType.MT, SectionType.ST)
HSS = (SectionType.HSS,)
PIPE = (SectionType.PIPE,)


@dataclass(frozen=True)
class SectionGeometry:
    """
    Type	Shape type: W, M, S, HP, C, MC, L, WT, MT, ST, 2L, HSS, PIPE
    EDI_ STD_ Nomenclature	The shape designation according to the AISC Naming Convention for Structural Steel Products
    AISC_  Manual_ Label	"The shape designation as seen in the AISC Steel Construction Manual, 15th Edition.  The exception to this is the designation for double angles. There is a separate listing (row) for each back-to-back spacing and configuration. Therefore, the shape designation reflects these two variables. The listings for double angles follow the convention specified in the AISC Naming Convention for Structural Steel Products for Use in Electronic Data Interchange (EDI), June 25, 2001."
    T_F	"Boolean variable. A true, T, value indicates that there is a special note for that shape (see below). A false, F, value indicates that there are no special notes for that shape.

    Special notes:
    W-shapes: a value of T for: tf > 2 in.\\
    M-shapes: a value of T indicates that the shape has sloped flanges.\\
    WT-shapes: a value of T for: tf > 2 in\\
    MT-shapes: a value of T indicates that the shape has sloped flanges.
    W	Nominal weight, lb/ft (kg/m)\\
    A	Cross-sectional area, in.2 (mm2)\\
    d	Overall depth of member, or width of shorter leg for angles, or width of the outstanding legs of long legs back-to-back double angles, or the width of the back-to-back legs of short legs back-to-back double angles, in. (mm)\\
    ddet	Detailing value of member depth, in. (mm)\\
    Ht	Overall depth of square or rectangular HSS, in. (mm)\\
    h	Depth of the flat wall of square or rectangular HSS, in. (mm)\\
    OD	Outside diameter of round HSS or pipe, in. (mm)\\
    bf	Flange width, in. (mm)\\
    bfdet	Detailing value of flange width, in. (mm)\\
    B	Overall width of square or rectangular HSS, in. (mm)\\
    b	Width of the flat wall of square or rectangular HSS, or width of the longer leg for angles, or width of the back-to-back legs of long legs back-to-back double angles, or width of the outstanding legs of short legs back-to-back double angles, in. (mm)\\
    ID	Inside diameter of round HSS or pipe, in. (mm)\\
    tw	Web thickness, in. (mm)\\
    twdet	Detailing value of web thickness, in. (mm)\\
    twdet/2	Detailing value of tw/2, in. (mm)\\
    tf	Flange thickness, in. (mm)\\
    tfdet	Detailing value of flange thickness, in. (mm)\\
    t	Thickness of angle leg, in. (mm)\\
    tnom	HSS and pipe nominal wall thickness, in. (mm)\\
    tdes	HSS and pipe design wall thickness, in. (mm)\\
    kdes	Design distance from outer face of flange to web toe of fillet, in. (mm)\\
    kdet	Detailing distance from outer face of flange to web toe of fillet, in. (mm)\\
    k1	Detailing distance from center of web to flange toe of fillet, in. (mm)\\
    x	Horizontal distance from designated member edge, as defined in the AISC Steel Construction Manual, to member centroidal axis, in. (mm)\\
    y	Vertical distance from designated member edge, as defined in the AISC Steel Construction Manual, to member centroidal axis, in. (mm)\\
    eo	Horizontal distance from designated member edge, as defined in the AISC Steel Construction Manual, to member shear center, in. (mm)\\
    xp	Horizontal distance from designated member edge, as defined in the AISC Steel Construction Manual, to member plastic neutral axis, in. (mm)\\
    yp	Vertical distance from designated member edge, as defined in the AISC Steel Construction Manual, to member plastic neutral axis, in. (mm)\\
    bf/2tf	Slenderness ratio\\
    b/t	Slenderness ratio for angles\\
    b/tdes	Slenderness ratio for square or rectangular HSS\\
    h/tw	Slenderness ratio\\
    h/tdes	Slenderness ratio for square or rectangular HSS\\
    D/t	Slenderness ratio for round HSS and pipe, or tee shapes\\
    Ix	Moment of inertia about the x-axis, in.4 (mm4 /106)\\
    Zx	Plastic section modulus about the x-axis, in.3 (mm3 /103)\\
    Sx	Elastic section modulus about the x-axis, in.3 (mm3 /103)\\
    rx	Radius of gyration about the x-axis, in. (mm)\\
    Iy	Moment of inertia about the y-axis, in.4 (mm4 /106)\\
    Zy	Plastic section modulus about the y-axis, in.3 (mm3 /103)\\
    Sy	Elastic section modulus about the y-axis, in.3 (mm3 /103)\\
    ry	Radius of gyration about the y-axis (with no separation for double angles back-to-back), in. (mm)\\
    Iz	Moment of inertia about the z-axis, in.4 (mm4 /106)\\
    rz	Radius of gyration about the z-axis, in. (mm)\\
    Sz	Elastic section modulus about the z-axis, in.3 (mm3 /103)\\
    J	Torsional moment of inertia, in.4 (mm4 /103)\\
    Cw	Warping constant, in.6 (mm6 /109)\\
    C	HSS torsional constant, in.3 (mm3 /103)\\
    Wno	Normalized warping function, as used in Design Guide 9, in.2 (mm2)\\
    Sw1	Warping statical moment at point 1 on cross section, as used in AISC Design Guide 9 and shown in Figures 1 and 2, in.4 (mm4 /106)\\
    Sw2	Warping statical moment at point 2 on cross section, as used in AISC Design Guide 9 and shown in Figure 2, in.4 (mm4 /106)\\
    Sw3	Warping statical moment at point 3 on cross section, as used in AISC Design Guide 9 and shown in Figure 2, in.4 (mm4 /106)\\
    Qf	Statical moment for a point in the flange directly above the vertical edge of the web, as used in AISC Design Guide 9, in.3 (mm3 /103)\\
    Qw	Statical moment for a point at mid-depth of the cross section, as used in AISC Design Guide 9, in.3 (mm3 /103)\\
    ro	Polar radius of gyration about the shear center, in. (mm)\\
    H	Flexural constant\\
    tan(α)	Tangent of the angle between the y-y and z-z axes for single angles, where a is shown in Figure 3\\
    Iw	Moment of inertia about the w-axis for single angles, in.4 (mm4 /106)\\
    zA	Distance from point A to center of gravity along z-axis, as shown in Figure 3, in. (mm)\\
    zB	Distance from point B to center of gravity along z-axis, as shown in Figure 3, in. (mm)\\
    zC	Distance from point C to center of gravity along z-axis, as shown in Figure 3, in. (mm)\\
    wA	Distance from point A to center of gravity along w-axis, as shown in Figure 3, in. (mm)\\
    wB	Distance from point B to center of gravity along w-axis, as shown in Figure 3, in. (mm)\\
    wC	Distance from point C to center of gravity along w-axis, as shown in Figure 3, in. (mm)\\
    SwA	Elastic section modulus about the w-axis at point A on cross section, as shown in Figure 3, in.3 (mm3 /103)\\
    SwB	Elastic section modulus about the w-axis at point B on cross section, as shown in Figure 3, in.3 (mm3 /103)\\
    SwC	Elastic section modulus about the w-axis at point C on cross section, as shown in Figure 3, in.3 (mm3 /103)\\
    SzA	Elastic section modulus about the z-axis at point A on cross section, as shown in Figure 3, in.3 (mm3 /103)\\
    SzB	Elastic section modulus about the z-axis at point B on cross section, as shown in Figure 3, in.3 (mm3 /103)\\
    SzC	Elastic section modulus about the z-axis at point C on cross section, as shown in Figure 3, in.3 (mm3 /103)\\
    rts	Effective radius of gyration, in. (mm)\\
    ho	Distance between the flange centroids, in. (mm)\\
    PA	Shape perimeter minus one flange surface (or short leg surface for a single angle), as used in Design Guide 19, in. (mm)\\
    PA2	Single angle shape perimeter minus long leg surface, as used in AISC Design Guide 19, in. (mm)\\
    PB	Shape perimeter, as used in AISC Design Guide 19, in. (mm)\\
    PC	Box perimeter minus one flange surface, as used in Design Guide 19, in. (mm)\\
    PD	Box perimeter, as used in AISC Design Guide 19, in. (mm)\\
    T	Distance between web toes of fillets at top and bottom of web, in. (mm)\\
    WGi	The workable gage for the inner fastener holes in the flange that provides for entering and tightening clearances and edge distance and spacing requirements. The actual size, combination, and orientation of fastener components should be compared with the geometry of the cross section to ensure compatibility. See AISC Manual Part 1 for additional information, in. (mm)\\
    WGo	The bolt spacing between inner and outer fastener holes when the workable gage is compatible with four holes across the flange. See AISC Manual Part 1 for additional information, in. (mm)\\
    """

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
    Ht: Quantity
    h: Quantity
    OD: Quantity
    bf: Quantity
    bfdet: Quantity
    B: Quantity
    b: Quantity
    ID: Quantity
    tw: Quantity
    twdet: Quantity
    twdet_2: Quantity
    tf: Quantity
    tfdet: Quantity
    t: Quantity
    tnom: Quantity
    tdes: Quantity
    kdes: Quantity
    kdet: Quantity
    k1: Quantity
    x: Quantity
    y: Quantity
    eo: Quantity
    xp: Quantity
    yp: Quantity
    bf_2tf: float
    b_t: float
    b_tdes: float
    h_tw: float
    h_tdes: float
    D_t: float
    Ix: Quantity
    Zx: Quantity
    Sx: Quantity
    rx: Quantity
    Iy: Quantity
    Zy: Quantity
    Sy: Quantity
    ry: Quantity
    Iz: Quantity
    rz: Quantity
    Sz: Quantity
    J: Quantity
    Cw: Quantity
    C: Quantity
    Wno: Quantity
    Sw1: Quantity
    Sw2: Quantity
    Sw3: Quantity
    Qf: Quantity
    Qw: Quantity
    ro: Quantity
    H: float
    tan_alpha: float
    Iw: Quantity
    zA: Quantity
    zB: Quantity
    zC: Quantity
    wA: Quantity
    wB: Quantity
    wC: Quantity
    SwA: Quantity
    SwB: Quantity
    SwC: Quantity
    SzA: Quantity
    SzB: Quantity
    SzC: Quantity
    rts: Quantity
    ho: Quantity
    PA: Quantity
    PA2: Quantity
    PB: Quantity
    PC: Quantity
    PD: Quantity
    T: Quantity
    WGi: Quantity
    WGo: Quantity


def _get_min_design_strength(
    criteria: dict[StrengthType, StrengthMixin],
) -> tuple[Quantity, StrengthType]:
    d = {key: value.design_strength for key, value in criteria.items()}
    key = min(d, key=d.get)
    return d[key], key


@dataclass
class LoadStrengthCalculation:
    criteria: dict[StrengthType, StrengthMixin]

    @property
    def design_strength_tuple(self):
        return _get_min_design_strength(self.criteria)

    @property
    def design_strength(self) -> Quantity:
        return self.design_strength_tuple[0]

    @property
    def design_strength_criterion(self) -> StrengthType:
        return self.design_strength_tuple[1]

    @property
    def design_strength_calculation(self) -> StrengthMixin:
        return self.criteria[self.design_strength_criterion]

    @property
    def strengths(self):
        return {
            key.value: value.design_strength for key, value in self.criteria.items()
        }


class ConstructionType(str, Enum):
    ROLLED = "ROLLED"
    BUILT_UP = "BUILT_UP"


class Connection(Protocol):
    @property
    def area_reduction(self) -> Quantity: ...

    @property
    def shear_lag_factor(self) -> float: ...


# class Section(Protocol):
#     geometry: SectionGeometry
#     material: Material
#     construction: ConstructionType

#     @abstractmethod
#     def compression(
#         self,
#         length_major_axis: Quantity,
#         factor_k_major_axis: float = 1.0,
#         length_minor_axis: Quantity = None,
#         factor_k_minor_axis: float = 1.0,
#         length_torsion: Quantity = None,
#         factor_k_torsion: float = 1.0,
#         design_type: DesignType = DesignType.ASD,
#         rule_editon: RuleEd = RuleEd.TWENTY_SIXTEEN,
#     ) -> LoadStrengthCalculation: ...

#     @abstractmethod
#     def flexure_major_axis(
#         length: Quantity,
#         design_type: DesignType = DesignType.ASD,
#         rule_editon: RuleEd = RuleEd.TWENTY_SIXTEEN,
#     ) -> LoadStrengthCalculation: ...

#     @abstractmethod
#     def flexure_minor_axis(
#         design_type: DesignType = DesignType.ASD,
#         rule_editon: RuleEd = RuleEd.TWENTY_SIXTEEN,
#     ) -> LoadStrengthCalculation: ...

#     @abstractmethod
#     def shear_major_axis(
#         design_type: DesignType = DesignType.ASD,
#         rule_editon: RuleEd = RuleEd.TWENTY_SIXTEEN,
#     ) -> LoadStrengthCalculation: ...

#     @abstractmethod
#     def shear_minor_axis(
#         design_type: DesignType = DesignType.ASD,
#         rule_editon: RuleEd = RuleEd.TWENTY_SIXTEEN,
#     ) -> LoadStrengthCalculation: ...
