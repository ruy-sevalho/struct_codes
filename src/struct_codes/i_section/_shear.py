from dataclasses import dataclass

from pint import Quantity

from struct_codes.criteria import DesignType, StrengthMixin
from struct_codes.sections import ConstructionType


def nominal_shear_strength(
    yield_stress: Quantity,
    web_area: Quantity,
    web_shear_coefficient: float = 1.0,
):
    return 0.6 * yield_stress * web_area * web_shear_coefficient


def web_shear_coefficient_limit_rolled(
    modulus_linear: Quantity,
    yield_stress: Quantity,
) -> float:
    """Condition of eq.G2-2 aisc 360-16"""
    return 2.24 * (modulus_linear / yield_stress) ** 0.5


def web_shear_coefficient_limit(
    shear_buckling_coefficient: float,
    modulus_linear: Quantity,
    yield_stress: Quantity,
) -> float:
    """Condition of eq. G2-3 aisc 360-16"""
    return 1.10 * (shear_buckling_coefficient * modulus_linear / yield_stress) ** 0.5


def web_shear_coefficient(
    shear_buckling_coefficient: float,
    modulus_linear: Quantity,
    yield_stress: Quantity,
    web_ratio: float,
) -> float:
    """eq. G2-4 aisc 360-16"""
    return (
        1.10
        * (shear_buckling_coefficient * modulus_linear / yield_stress) ** 0.5
        / web_ratio
    )


@dataclass
class WebShearCalculation2016(StrengthMixin):
    yield_stress: Quantity
    modulus: Quantity
    web_area: Quantity
    web_ratio: float
    construction_type: ConstructionType
    web_plate_shear_buckling_coefficient: float = 5.34
    design_type: DesignType = DesignType.ASD

    @property
    def rolled_web_ratio_limit(self):
        return web_shear_coefficient_limit_rolled(
            modulus_linear=self.modulus,
            yield_stress=self.yield_stress,
        )

    @property
    def _web_shear_strength_coefficient(self):
        return web_shear_coefficient(
            shear_buckling_coefficient=self.web_plate_shear_buckling_coefficient,
            modulus_linear=self.modulus,
            yield_stress=self.yield_stress,
            web_ratio=self.web_ratio,
        )

    @property
    def web_shear_strength_coefficient_limit(self):
        return web_shear_coefficient_limit(
            shear_buckling_coefficient=self.web_plate_shear_buckling_coefficient,
            modulus_linear=self.modulus,
            yield_stress=self.yield_stress,
        )

    @property
    def web_shear_strength_coefficient(self):
        if (
            self.construction_type == ConstructionType.ROLLED
            and self.web_ratio <= self.rolled_web_ratio_limit
        ):
            self.asd_factor = 1.50
            self.lrfd_factor = 1.0
            return 1
        if self.web_ratio <= self.web_shear_strength_coefficient_limit:
            return 1
        return self._web_shear_strength_coefficient

    @property
    def nominal_strength(self):
        return nominal_shear_strength(
            yield_stress=self.yield_stress,
            web_area=self.web_area,
            web_shear_coefficient=self.web_shear_strength_coefficient,
        )

    @property
    def calculation_memory(self):
        return WebShearCalculationMemory2016(
            nominal_strength=self.nominal_strength,
            design_strength=self.design_strength,
            web_shear_strength_coefficient=self.web_shear_strength_coefficient,
        )


@dataclass
class WebShearCalculationMemory2016:
    nominal_strength: Quantity
    design_strength: Quantity
    web_shear_strength_coefficient: Quantity
