# %%
import json

from struct_codes.aisc_database import (
    aisc_sections_15ed,
    aisc_sections_16ed,
    create_aisc_section,
)
from struct_codes.criteria import StrengthType
from struct_codes.i_section import DoublySymmetricI
from struct_codes.materials import steel250MPa
from struct_codes.sections import ConstructionType
from struct_codes.units import meter, newton

# %%
# s: DoublySymmetricI = create_aisc_section(
#     "W44X335", steel250MPa, ConstructionType.ROLLED
# )
# strength = s.compression(length_major_axis=10*meter).strengths
# print(strength)
# %%
print(aisc_sections_15ed["C15X50"])
# %%
