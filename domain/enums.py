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
    NC = "0"
    E6 = "1"
    E5 = "2"
    E4 = "3"
    E3 = "4"
    E2 = "5"
    E1 = "6"
    E0 = "7"
    D6 = "8"
    D5 = "9"
    D4 = "10"
    D3 = "11"
    D2 = "12"
    D1 = "13"
    D0 = "14"
    C6 = "15"
    C5 = "16"
    C4 = "17"
    C3 = "18"
    C2 = "19"
    C1 = "20"
    C0 = "21"
    B6 = "22"
    B5 = "23"
    B4 = "24"
    B3 = "25"
    B2 = "26"
    B1 = "27"
    B0 = "28"
