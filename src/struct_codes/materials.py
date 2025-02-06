from dataclasses import dataclass
from typing import Protocol

from pint import Quantity

from struct_codes.units import gigapascal, megapascal


@dataclass
class Material(Protocol):
    modulus_linear: Quantity
    modulus_shear: Quantity
    poisson_ratio: float
    yield_strength: Quantity
    ultimate_strength: Quantity


@dataclass
class UserDefiniedMaterial(Material):
    modulus_linear: Quantity
    modulus_shear: Quantity
    poisson_ratio: float
    yield_strength: Quantity
    ultimate_strength: Quantity
    density: Quantity | None = None


steel355MPa = UserDefiniedMaterial(
    modulus_linear=200 * gigapascal,
    modulus_shear=77 * gigapascal,
    poisson_ratio=0.3,
    yield_strength=355 * megapascal,
    ultimate_strength=500 * megapascal,
)
