from abc import ABC
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Protocol

from struct_codes.criteria import DesignType, StrengthType
from struct_codes.units import Quantity


@dataclass
class CalcMemory(Protocol): ...


@dataclass
class StrengthCalculation(Protocol):
    @property
    def desing_strength(self) -> Quantity: ...

    @property
    def calculation_memory(self) -> CalcMemory: ...


@dataclass
class CalculationCollection(Protocol):
    @property
    def to_dict(self) -> dict[StrengthType, StrengthCalculation]:
        return asdict(self)

    @property
    def desing_strenght_tuple(self):
        return get_max_design_strength_tuple(self)

    @property
    def desing_strengt(self) -> Quantity:
        return self.desing_strenght_tuple[0]


def get_max_design_strength_tuple(collecion: CalculationCollection):
    d = {key: value.desing_strength for key, value in collecion.to_dict.items()}
    key = max(d, key=d.get)
    return d[key], key


def _get_min_design_strength(
    criteria: dict[StrengthType, StrengthCalculation],
) -> tuple[Quantity, StrengthType]:
    d = {key: value.desing_strength for key, value in criteria.items()}
    key = min(d, d.get)
    return d[key], key


@dataclass
class LoadStrengthCalculation:
    criteria: dict[StrengthType, StrengthCalculation]

    @property
    def design_strength_tuple(self) -> Quantity:
        return _get_min_design_strength(self.criteria)

    @property
    def design_strength(self) -> Quantity:
        return self.design_strength_tuple[0]

    @property
    def design_strength_criterion(self) -> StrengthType:
        return self.design_strength_tuple[1]


class LoadCheck(Protocol):
    criteria: CalculationCollection

    @property
    def calculation_memories(self) -> dict[StrengthType, CalcMemory]: ...

    @property
    def design_strength(self) -> Quantity: ...

    @property
    def calculation_memory(self) -> CalcMemory: ...


class Section(Protocol):
    def slenderness(self): ...

    @property
    def slenderness_2016(self):
        pass

    @property
    def slenderness_calc_memory_2016(self):
        pass

    def tension(
        self, design_type: DesignType = DesignType.ASD
    ) -> LoadStrengthCalculation: ...

    def tension_calc_memory_2016(self, design_type: DesignType): ...

    def compression_calc_memory_2016(
        length_major_axis: Quantity,
        factor_k_major_axis: float = 1.0,
        length_minor_axis: Quantity = None,
        factor_k_minor_axis: float = 1.0,
        length_torsion: Quantity = None,
        factor_k_torsion: float = 1.0,
        design_type: DesignType = DesignType.ASD,
    ) -> LoadCheck: ...


class Geo(Protocol):
    tf: Quantity


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


class ConstructionType(str, Enum):
    ROLLED = "ROLLED"
    BUILT_UP = "BUILT_UP"


class Connection(Protocol):
    @property
    def area_reduction(self) -> Quantity: ...

    @property
    def shear_lag_factor(self) -> float: ...
