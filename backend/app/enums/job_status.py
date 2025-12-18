from enum import IntEnum, unique


@unique
class JobStatus(IntEnum):
    SAVED = 1
    APPLIED = 2
    INTERVIEW = 3
    REJECTED = 4
    DECLINED = 5
    OFFER = 6
