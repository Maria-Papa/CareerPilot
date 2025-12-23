from enum import StrEnum, unique


@unique
class InterviewOutcome(StrEnum):
    PENDING = "PENDING"
    PASSED = "PASSED"
    FAILED = "FAILED"
    OFFERED = "OFFERED"
    CANCELED = "CANCELED"
    NO_SHOW = "NO_SHOW"
