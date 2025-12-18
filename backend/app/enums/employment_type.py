from enum import IntEnum, unique


@unique
class EmploymentType(IntEnum):
    FULL_TIME = 1
    PART_TIME = 2
    CONTRACT = 3
    FREELANCE = 4
    INTERN = 5
    TEMPORARY = 6
