# %%
import types
from enum import Enum, StrEnum
from pathlib import Path

from struct_codes.aisc_database import aisc_sections_15ed

section_names = [n for n in aisc_sections_15ed.keys()]
