from enum import StrEnum, auto


class BracketType(StrEnum):
    JUNIOR = auto()
    BEGINNER = auto()
    INTERMADIATE = auto()
    EXPERT = auto()


class MatchType(StrEnum):
    POOL = auto()
    ROUND_OF_32 = auto()
    ROUND_OF_16 = auto()
    QUARTER = auto()
    SEMI_FINAL = auto()
    FINAL = auto()


class FederationRanking(StrEnum):
    NC = "NC"
    E6 = "E6"
    E5 = "E5"
    E4 = "E4"
    E3 = "E3"
    E2 = "E2"
    E1 = "E1"
    E0 = "E0"
    D6 = "D6"
    D5 = "D5"
    D4 = "D4"
    D3 = "D3"
    D2 = "D2"
    D1 = "D1"
    D0 = "D0"
    C6 = "C6"
    C5 = "C5"
    C4 = "C4"
    C3 = "C3"
    C2 = "C2"
    C1 = "C1"
    C0 = "C0"
    B6 = "B6"
    B5 = "B5"
    B4 = "B4"
    B3 = "B3"
    B2 = "B2"
    B1 = "B1"
    B0 = "B0"
