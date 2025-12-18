from enum import IntEnum, unique


@unique
class InterviewOutcome(IntEnum):
    PENDING = 0
    PASSED = 1
    FAILED = 2
    OFFERED = 3
    CANCELED = 4
