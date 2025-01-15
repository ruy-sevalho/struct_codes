from dataclasses import dataclass
from typing import Protocol

from pint import Quantity

from struct_codes.units import giga_pascal, mega_pascal


@dataclass
class Material(Protocol):
    modulus_linear: Quantity
    modulus_shear: Quantity
    poisson_ratio: float
    yield_strength: Quantity


@dataclass
class UserDefiniedMaterial(Material):
    modulus_linear: Quantity
    modulus_shear: Quantity
    poisson_ratio: float
    yield_strength: Quantity
    density: Quantity | None = None


steel355MPa = UserDefiniedMaterial(
    modulus_linear=200 * giga_pascal,
    modulus_shear=77 * giga_pascal,
    poisson_ratio=0.3,
    yield_strength=355 * mega_pascal,
)
