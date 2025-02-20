import os
from dataclasses import make_dataclass
from pathlib import Path

from pint import Quantity

from struct_codes.aisc_database import AISC_Sections
from struct_codes.units import meter

section_names = AISC_Sections.keys()
print(section_names)
with open(Path("aisc_sections"), "w") as file:
    file.write(AISC_Sections.__repr__())
