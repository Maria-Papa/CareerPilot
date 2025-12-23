from enum import StrEnum, unique


@unique
class FileType(StrEnum):
    CV = "CV"
    COVER_LETTER = "COVER_LETTER"
    PORTFOLIO = "PORTFOLIO"
    ASSIGNMENT = "ASSIGNMENT"
    REFERENCES = "REFERENCES"
    OTHER = "OTHER"
