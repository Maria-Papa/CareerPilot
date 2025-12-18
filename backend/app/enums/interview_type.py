from enum import IntEnum, unique


@unique
class InterviewType(IntEnum):
    HR_SCREEN = 1
    PHONE_SCREEN = 2
    TECHNICAL = 3
    SYSTEM_DESIGN = 4
    TAKE_HOME = 5
    PAIR_PROGRAMMING = 6
    MANAGER = 7
    FINAL = 8
    OFFER_DISCUSSION = 9
