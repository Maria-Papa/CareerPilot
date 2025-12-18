from enum import IntEnum, unique


@unique
class JobEventType(IntEnum):
    NOTE = 1
    APPLICATION_SUBMITTED = 2
    INTERVIEW_SCHEDULED = 3
    EMAIL_RECEIVED = 4
    SALARY_UPDATE = 5
