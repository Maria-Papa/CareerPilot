from enum import StrEnum, unique


@unique
class FlexibilityType(StrEnum):
    ON_SITE = "ON_SITE"
    HYBRID = "HYBRID"
    REMOTE = "REMOTE"
