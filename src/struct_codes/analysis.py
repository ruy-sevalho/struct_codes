from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Iterable, Protocol

from struct_codes.beam import Beam
from struct_codes.compression import compression_criteria_table
from struct_codes.criteria import DesignType, Strength, StrengthType
from struct_codes.materials import Material
from struct_codes.sections import (
    Connection,
    ConstructionType,
    LoadStrengthCalculation,
    SectionClassification,
    SectionGeometry,
)
from struct_codes.units import Quantity


class BeamAnalyisGeneral(ABC):
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
class AnalysisInput:
    geometry: SectionGeometry
    section_type: SectionClassification
    material: Material
    construction: ConstructionType
    beam: Beam
    design_type: DesignType
    connection: Connection = None
    


    # @property
    # def compression(self):
    #     return load_check(self, compression_criteria_table)
    
    @abstractmethod
    def compression(self) -> LoadStrengthCalculation:
        ...




# def load_check(
#     model: Analysis,
#     criteria_per_section_table: dict[
#         SectionClassification,
#         Iterable[
#             tuple[
#                 StrengthType,
#                 Callable[
#                     [
#                         Analysis,
#                     ],
#                     Strength,
#                 ],
#             ]
#         ],
#     ],
# ):
#     criteria_list = criteria_per_section_table[model.section_type]
#     criteria_dict = {name: criteria(model) for name, criteria in criteria_list}
#     return LoadStrengthCalculation(criteria=criteria_dict)


if __name__ == "__main__":
    # Analysis()
