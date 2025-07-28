from struct_codes.criteria import StrengthType
from struct_codes.sections import SectionClassification
from struct_codes.slenderness import Slenderness

SECTION = "section"
FLANGE_SLENDERNESS = "flange_slenderness"
WEB_SLENDERNESS = "web_slenderness"


def look_up_limit_states(data):
    match data:
        case (
            SectionClassification.DOUBLY_SYMMETRIC_I | SectionClassification.CHANEL,
            Slenderness.COMPACT,
            Slenderness.COMPACT,
        ):
            return StrengthType.YIELD, StrengthType.LATERAL_TORSIONAL_BUCKLING
        case _:
            raise ValueError(f"{data} configuration of analysis is not valid")


if __name__ == "__main__":
    print(
        look_up_limit_states(
            (
                SectionClassification.DOUBLY_SYMMETRIC_I,
                Slenderness.COMPACT,
                Slenderness.COMPACT,
            )
        )
    )
