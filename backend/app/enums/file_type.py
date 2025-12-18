from enum import IntEnum, unique


@unique
class FileType(IntEnum):
    CV = 1
    COVER_LETTER = 2
    PORTFOLIO = 3
    ASSIGNMENT = 4
    OTHER = 99
