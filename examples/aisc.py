# %%
from encodings.punycode import T
from re import U
from struct_codes.aisc_database import create_aisc_section
from struct_codes.i_section import DoublySymmetricI
from struct_codes.materials import steel250MPa
from struct_codes.sections import ConstructionType
from struct_codes.units import meter, newton

# %%
s: DoublySymmetricI = create_aisc_section(
    "W44X335", steel250MPa, ConstructionType.ROLLED
)
strength, failure_mode = s.compression(length_major_axis=10*meter).design_strength_tuple
print(f"avaliable strength: {strength.to(newton)}, failure mode: {failure_mode.value}")
