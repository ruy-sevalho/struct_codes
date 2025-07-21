from abc import abstractmethod
from calendar import c
from dataclasses import dataclass
from typing import Protocol

from struct_codes.aisc_database import AISC_SECTIONS_15ED
from struct_codes.beam import Beam, BeamElement
from struct_codes.compression import compreesion
from struct_codes.materials import Material
from struct_codes.sections import (
    AiscSectionGeometry,
    ConstructionType,
    LoadStrengthCalculation,
    SectionClassification,
)
from struct_codes.units import Quantity


class BeamAnalyisGeneral(Protocol):
    @abstractmethod
    def compression(self, load: Quantity) -> LoadStrengthCalculation: ...

    @abstractmethod
    def tension(self, load: Quantity) -> LoadStrengthCalculation: ...


class BeamAnalysisMajorMinorAxis(Protocol):
    @abstractmethod
    def bending_major_axis(
        self, lateral_torsion_mod_factor: float = None
    ) -> LoadStrengthCalculation:
        pass

    @abstractmethod
    def bending_minor_axis(self) -> LoadStrengthCalculation:
        pass

    @abstractmethod
    def shear_major_axis(self) -> LoadStrengthCalculation:
        pass

    @abstractmethod
    def shear_minor_axis(self) -> LoadStrengthCalculation:
        pass


class BeamAnalysisPipe(Protocol):
    @abstractmethod
    def bending(self) -> LoadStrengthCalculation:
        pass

    @abstractmethod
    def shear(self) -> LoadStrengthCalculation:
        pass


@dataclass
class Analysis(BeamElement):
    def compression(self):
        return compreesion(self)


if __name__ == "__main__":
    pass
