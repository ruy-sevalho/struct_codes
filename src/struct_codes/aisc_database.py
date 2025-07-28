from dataclasses import fields
from math import isnan
from pathlib import Path
from typing import Any

import pandas as pd

from struct_codes.i_section import DoublySymmetricI, DoublySymmetricIGeo
from struct_codes.materials import Material
from struct_codes.sections import (
    AiscSectionGeometry,
    ConstructionType,
    RuleEd,
    SectionType,
    section_table,
)
from struct_codes.units import Quantity, kilogram, meter, millimeter

DATABASE_PATH_16ed = Path(__file__).parent / Path("aisc-shapes-database-v16.0.csv")
DATABASE_PATH_15ed = Path(__file__).parent / Path("aisc-shapes-database-v15.0.csv")

LENGTH = "length"
AREA = "area"
INERTIA = "inertia"
SECTION_MODULUS = "section_modulus"
LINEAR_WEIGHT = "linear_weight"
TORSIONAL_INERTIA = "torsional_inertia"
WARPING_CONSTANT = "warping_constant"
HSS_TORSIONAL_CONSTANT = "hss_torsional_constant"

CONVERSION_FACTORS = {
    LENGTH: (millimeter, 1.0),
    AREA: (millimeter**2, 1.0),
    LINEAR_WEIGHT: (kilogram / meter, 1.0),
    INERTIA: (millimeter**4, 10**6),
    SECTION_MODULUS: (millimeter**3, 10**3),
    TORSIONAL_INERTIA: (millimeter**4, 10**3),
    WARPING_CONSTANT: (millimeter**6, 10**9),
    HSS_TORSIONAL_CONSTANT: (millimeter**3, 10**3),
}

PARAMS = {
    "EDI_STD_Nomenclature_imp": str,
    "AISC_Manual_Label_imp": str,
    "EDI_STD_Nomenclature_metric": str,
    "AISC_Manual_Label_metric": str,
    "type": str,
    "T_F": bool,
    "W": LINEAR_WEIGHT,
    "A": AREA,
    "d": LENGTH,
    "ddet": LENGTH,
    "Ht": LENGTH,
    "h": LENGTH,
    "OD": LENGTH,
    "bf": LENGTH,
    "bfdet": LENGTH,
    "B": LENGTH,
    "b": LENGTH,
    "ID": LENGTH,
    "tw": LENGTH,
    "twdet": LENGTH,
    "twdet_2": LENGTH,
    "tf": LENGTH,
    "tfdet": LENGTH,
    "t": LENGTH,
    "tnom": LENGTH,
    "tdes": LENGTH,
    "kdes": LENGTH,
    "kdet": LENGTH,
    "k1": LENGTH,
    "x": LENGTH,
    "y": LENGTH,
    "eo": LENGTH,
    "xp": LENGTH,
    "yp": LENGTH,
    "bf_2tf": float,
    "b_t": float,
    "b_tdes": float,
    "h_tw": float,
    "h_tdes": float,
    "D_t": float,
    "Ix": INERTIA,
    "Zx": SECTION_MODULUS,
    "Sx": SECTION_MODULUS,
    "rx": LENGTH,
    "Iy": INERTIA,
    "Zy": SECTION_MODULUS,
    "Sy": SECTION_MODULUS,
    "ry": LENGTH,
    "Iz": INERTIA,
    "rz": LENGTH,
    "Sz": SECTION_MODULUS,
    "J": TORSIONAL_INERTIA,
    "Cw": WARPING_CONSTANT,
    "C": HSS_TORSIONAL_CONSTANT,
    "Wno": AREA,
    "Sw1": INERTIA,
    "Sw2": INERTIA,
    "Sw3": INERTIA,
    "Qf": SECTION_MODULUS,
    "Qw": SECTION_MODULUS,
    "ro": LENGTH,
    "H": float,
    "tan_alpha": float,
    "Iw": INERTIA,
    "zA": LENGTH,
    "zB": LENGTH,
    "zC": LENGTH,
    "wA": LENGTH,
    "wB": LENGTH,
    "wC": LENGTH,
    "SwA": SECTION_MODULUS,
    "SwB": SECTION_MODULUS,
    "SwC": SECTION_MODULUS,
    "SzA": SECTION_MODULUS,
    "SzB": SECTION_MODULUS,
    "SzC": SECTION_MODULUS,
    "rts": LENGTH,
    "ho": LENGTH,
    "PA": LENGTH,
    "PA2": LENGTH,
    "PB": LENGTH,
    "PC": LENGTH,
    "PD": LENGTH,
    "T": LENGTH,
    "WGi": LENGTH,
    "WGo": LENGTH,
}


def convert(value: float, unit: Quantity, factor: float = 1) -> Quantity:
    return float(value) * factor * unit


def process_entry(name: str, value: Any):
    typ = PARAMS[name]
    if isinstance(value, float) and isnan(value):
        return None
    if typ in CONVERSION_FACTORS:
        unit, factor = CONVERSION_FACTORS[typ]
        return float(value) * factor * unit
    if typ is bool:
        table = {
            "T": True,
            "F": False,
        }
        return table.get(value, False)
    return value


def process_aisc_database_v160_row(section: dict[str, Any]):
    return {name: process_entry(name, value) for name, value in section.items()}


def read_csv_table(file_path: Path):
    with open(file_path, "r") as f:
        df = pd.read_csv(f, na_values="–")

    # dropping values in Imperial units

    df = df.drop(
        columns=[
            "W",
            "A",
            "d",
            "ddet",
            "Ht",
            "h",
            "OD",
            "bf",
            "bfdet",
            "B",
            "b",
            "ID",
            "tw",
            "twdet",
            "twdet/2",
            "tf",
            "tfdet",
            "t",
            "tnom",
            "tdes",
            "kdes",
            "kdet",
            "k1",
            "x",
            "y",
            "eo",
            "xp",
            "yp",
            "bf/2tf",
            "b/t",
            "b/tdes",
            "h/tw",
            "h/tdes",
            "D/t",
            "Ix",
            "Zx",
            "Sx",
            "rx",
            "Iy",
            "Zy",
            "Sy",
            "ry",
            "Iz",
            "rz",
            "Sz",
            "J",
            "Cw",
            "C",
            "Wno",
            "Sw1",
            "Sw2",
            "Sw3",
            "Qf",
            "Qw",
            "ro",
            "H",
            "tan(?)",
            "Iw",
            "zA",
            "zB",
            "zC",
            "wA",
            "wB",
            "wC",
            "SwA",
            "SwB",
            "SwC",
            "SzA",
            "SzB",
            "SzC",
            "rts",
            "ho",
            "PA",
            "PA2",
            "PB",
            "PC",
            "PD",
            "T",
            "WGi",
            "WGo",
        ]
    )

    # renaming columns, remove .1 from metric values and substitute invalid "/" character
    df.rename(
        columns={name: name[:-2].replace("/", "_") for name in list(df.columns)[6:]},
        inplace=True,
    )

    # other label corrections
    df.rename(
        columns={
            "tan(?)": "tan_alpha",
            "EDI_Std_Nomenclature": "EDI_STD_Nomenclature_imp",
            "AISC_Manual_Label": "AISC_Manual_Label_imp",
            "EDI_Std_Nomenclature.1": "EDI_STD_Nomenclature_metric",
            "AISC_Manual_Label.1": "AISC_Manual_Label_metric",
            "Type": "type",
        },
        inplace=True,
    )
    return convert_inputs(df)


def read_json_cleaned_up_file(file_path: Path):
    df = pd.read_json(file_path)
    return convert_inputs(df)


def convert_inputs(df: pd.DataFrame):
    return {
        row.EDI_STD_Nomenclature_imp: dict(
            **process_aisc_database_v160_row(
                {
                    key: value
                    for key, value in row._asdict().items()
                    # if not (isinstance(value, float) and isnan(value))
                }
            )
        )
        for row in df.itertuples(index=False)
    }


AISC_SECTIONS_16ED = read_csv_table(DATABASE_PATH_16ed)
AISC_SECTIONS_15ED = read_csv_table(DATABASE_PATH_15ed)

section_table_old = {SectionType.W: DoublySymmetricI}


def create_aisc_section(
    section_name: str, material: Material, construction: ConstructionType
):
    section_dict = AISC_SECTIONS_15ED[section_name]
    section_type = section_dict["type"]
    section_class = section_table_old[section_type]
    return section_class(
        geometry=AiscSectionGeometry(**section_dict),
        material=material,
        construction=construction,
    )


def get_aisc_section_geo_and_type(name: str, ed: RuleEd = RuleEd.ED15):
    section = {RuleEd.ED15: AISC_SECTIONS_15ED, RuleEd.ED16: AISC_SECTIONS_16ED}[ed][
        name
    ]
    return AiscSectionGeometry(**section), section_table[section["type"]]
