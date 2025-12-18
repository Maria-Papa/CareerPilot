from enum import IntEnum, unique


@unique
class FlexibilityType(IntEnum):
    ON_SITE = 1
    HYBRID = 2
    REMOTE = 3
