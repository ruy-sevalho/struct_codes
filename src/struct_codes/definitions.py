from enum import Enum
from typing import Protocol

from struct_codes.criteria import DesignType
from struct_codes.units import Quantity


class Section_2016(Protocol):
    @property
    def slenderness_2016(self):
        pass

    @property
    def slenderness_calc_memory_2016(self):
        pass

    def tension_calc_memory_2016(self, design_type: DesignType): ...


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
