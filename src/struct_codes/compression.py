from __future__ import annotations

import math
from abc import abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from typing import TYPE_CHECKING

from struct_codes.criteria import DesignType, Strength, StrengthType
from struct_codes.sections import LoadStrengthCalculation, SectionClassification
from struct_codes.units import Quantity

if TYPE_CHECKING:
    from struct_codes.analysis import Analysis


def member_slenderness_ratio(
    factor_k: float, unbraced_length: Quantity, radius_of_gyration: Quantity
) -> float:
    """E2. Effective length - aisc 360-16"""
    n = unbraced_length / radius_of_gyration
    return factor_k * n


def _nominal_compressive_strength(
    critical_stress: Quantity, sectional_area: Quantity
) -> Quantity:
    """E3. FLEXURAL BUCKLING OF MEMBERS WITHOUT SLENDER ELEMENTS (E3-1) - aisc 360-16"""
    return critical_stress * sectional_area


def critical_compression_stress_buckling_default(
    # member_slenderness: float,
    yield_stress: Quantity,
    elastic_buckling_stress: Quantity,
    # member_slenderness_limit: float,
) -> Quantity:
    """E3-2 and E3-3 - aisc 360-16"""
    if yield_stress / elastic_buckling_stress <= 2.25:
        # (E3-2)
        ratio = yield_stress / elastic_buckling_stress
        return 0.658**ratio * yield_stress
    # (E3-3)
    return 0.877 * elastic_buckling_stress


# E(3-4)
def elastic_flexural_buckling_stress(
    modulus_linear: Quantity, member_slenderness_ratio: float
) -> Quantity:
    """E3-4 - aisc 360-16"""
    return math.pi**2 * modulus_linear / member_slenderness_ratio**2


# (E4-2)
def elastic_torsional_buckling_stress_doubly_symmetric_member(
    modulus_linear: Quantity,
    modulus_shear: Quantity,
    factor_k: float,
    length: Quantity,
    torsional_constant: Quantity,
    major_axis_inertia: Quantity,
    minor_axis_inertia: Quantity,
    warping_constant: Quantity,
) -> Quantity:
    return (
        math.pi**2 * modulus_linear * warping_constant / (factor_k * length) ** 2
        + modulus_shear * torsional_constant
    ) * (1 / (minor_axis_inertia + major_axis_inertia))


# Note of page Sect. E4. TORSIONAL AND FLEXURAL-TORSIONAL BUCKLING OF MEMBERS
def doubly_symmetric_i_warping_constant(
    moment_of_inertia: Quantity, distance_between_flanges_centroid: Quantity
):
    return moment_of_inertia * distance_between_flanges_centroid**2 / 4


@dataclass
class BucklingStrengthCalculationMixin(Strength):
    yield_stress: Quantity
    gross_area: Quantity

    @property
    @abstractmethod
    def elastic_buckling_stress(self) -> Quantity:
        pass

    @property
    def critical_stress(self):
        return critical_compression_stress_buckling_default(
            elastic_buckling_stress=self.elastic_buckling_stress,
            yield_stress=self.yield_stress,
        )

    @property
    def nominal_strength(self) -> Quantity:
        return _nominal_compressive_strength(
            critical_stress=self.critical_stress,
            sectional_area=self.gross_area,
        )


@dataclass
class FlexuralBucklingStrengthCalculation(BucklingStrengthCalculationMixin):
    length: Quantity
    factor_k: Quantity
    yield_stress: Quantity
    modulus_linear: Quantity
    gross_area: Quantity
    radius_of_gyration: Quantity
    design_type: DesignType

    @property
    def beam_slenderness(self):
        return member_slenderness_ratio(
            factor_k=self.factor_k,
            radius_of_gyration=self.radius_of_gyration,
            unbraced_length=self.length,
        )

    @property
    def elastic_buckling_stress(self):
        return elastic_flexural_buckling_stress(
            modulus_linear=self.modulus_linear,
            member_slenderness_ratio=self.beam_slenderness,
        )


@dataclass
class TorsionalBucklingDoublySymmetricStrengthCalculation(
    BucklingStrengthCalculationMixin
):
    length: Quantity
    factor_k: Quantity
    yield_stress: Quantity
    modulus_linear: Quantity
    modulus_shear: Quantity
    gross_area: Quantity
    major_axis_inertia: Quantity
    minor_axis_inertia: Quantity
    torsional_constant: Quantity
    warping_constant: Quantity
    design_type: DesignType

    @property
    def elastic_buckling_stress(self):
        return elastic_torsional_buckling_stress_doubly_symmetric_member(
            modulus_linear=self.modulus_linear,
            modulus_shear=self.modulus_shear,
            factor_k=self.factor_k,
            length=self.length,
            torsional_constant=self.torsional_constant,
            major_axis_inertia=self.major_axis_inertia,
            minor_axis_inertia=self.minor_axis_inertia,
            warping_constant=self.warping_constant,
        )


@dataclass
class EffectiveWidthCalculation:
    yield_stress: Quantity
    critical_stress: Quantity
    width: Quantity
    slenderness: float
    limit_slenderness: float
    coefficient_1: float

    @property
    def effective_width(self):
        return None


@dataclass
class SymmetricFlangesFlexuralBuckling(FlexuralBucklingStrengthCalculation):
    flange_width: Quantity
    flange_thickness: Quantity
    flange_slenderss_limit: Quantity
    web_width: Quantity
    web_thickness: Quantity
    web_slenderss_limit: Quantity

    @property
    def effective_flange_width(self):
        return


def flexural_buckling_major_axis_default(model: Analysis):
    return FlexuralBucklingStrengthCalculation(
        length=model.beam.length_major_axis,
        factor_k=model.beam.factor_k_major_axis,
        yield_stress=model.material.yield_strength,
        modulus_linear=model.material.modulus_linear,
        gross_area=model.geometry.A,
        radius_of_gyration=model.geometry.rx,
        design_type=model.design_type,
    )


def flexural_buckling_minor_axis_default(model: Analysis):
    return FlexuralBucklingStrengthCalculation(
        length=model.beam.length_minor_axis,
        factor_k=model.beam.factor_k_minor_axis,
        yield_stress=model.material.yield_strength,
        modulus_linear=model.material.modulus_linear,
        gross_area=model.geometry.A,
        radius_of_gyration=model.geometry.ry,
        design_type=model.design_type,
    )


def torsional_buckling_doubly_symmtric_i(model: Analysis):
    return TorsionalBucklingDoublySymmetricStrengthCalculation(
        yield_stress=model.material.yield_strength,
        gross_area=model.geometry.A,
        length=model.beam.length_torsion,
        factor_k=model.beam.factor_k_torsion,
        modulus_linear=model.material.modulus_linear,
        modulus_shear=model.material.modulus_shear,
        major_axis_inertia=model.geometry.Ix,
        minor_axis_inertia=model.geometry.Iy,
        torsional_constant=model.geometry.J,
        warping_constant=model.geometry.Cw,
        design_type=model.design_type,
    )


default_flexural_buckling_major_axis = (
    StrengthType.FLEXURAL_BUCKLING_MAJOR_AXIS,
    flexural_buckling_major_axis_default,
)

default_flexural_buckling_minor_axis = (
    StrengthType.FLEXURAL_BUCKLING_MINOR_AXIS,
    flexural_buckling_minor_axis_default,
)


compression_criteria_table = {
    SectionClassification.DOUBLY_SYMMETRIC_I: (
        default_flexural_buckling_major_axis,
        default_flexural_buckling_minor_axis,
        (StrengthType.TORSIONAL_BUCKLING, torsional_buckling_doubly_symmtric_i),
    ),
    SectionClassification.SINGLY_SYMMETRIC_I: (
        default_flexural_buckling_major_axis,
        default_flexural_buckling_minor_axis,
        # (StrengthType.TORSIONAL_BUCKLING,)
    ),
    SectionClassification.CHANEL: (
        default_flexural_buckling_major_axis,
        default_flexural_buckling_minor_axis,
        # StrengthType.TORSIONAL_BUCKLING,
    ),
    SectionClassification.HSS: (
        default_flexural_buckling_major_axis,
        default_flexural_buckling_minor_axis,
    ),
    SectionClassification.PIPE: (
        default_flexural_buckling_major_axis,
        default_flexural_buckling_minor_axis,
    ),
    SectionClassification.ANGLE: (
        default_flexural_buckling_major_axis,
        default_flexural_buckling_minor_axis,
    ),
}


# flexural_buckling_major_axis_table = defaultdict(
#     lambda _: flexural_buckling_major_axis_default
# )
# flexural_buckling_minor_axis_table = defaultdict(
#     lambda _: flexural_buckling_minor_axis_default
# )
# torsional_buckling_table = {
#     SectionClassification.DOUBLY_SYMMETRIC_I: torsional_buckling_doubly_symmtric_i,
# }
# table_criteria_per_section_type = {
#     StrengthType.FLEXURAL_BUCKLING_MAJOR_AXIS: flexural_buckling_major_axis_table,
#     StrengthType.FLEXURAL_BUCKLING_MINOR_AXIS: flexural_buckling_minor_axis_table,
#     StrengthType.TORSIONAL_BUCKLING: torsional_buckling_table,
# }


# def compreesion(model: BeamElement):
#     criteria_list = compression_criteria_table[model.section_type]
#     criteria_dict = dict()
#     for criteria in criteria_list:
#         criteria_dict.update(
#             {
#                 criteria: table_criteria_per_section_type[criteria][model.section_type](
#                     model
#                 )
#             }
#         )
#     return LoadStrengthCalculation(criteria=criteria_dict)
