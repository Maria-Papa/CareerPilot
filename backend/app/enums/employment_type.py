from enum import StrEnum, unique


@unique
class EmploymentType(StrEnum):
    FULL_TIME = "FULL_TIME"
    PART_TIME = "PART_TIME"
    CONTRACT = "CONTRACT"
    FREELANCE = "FREELANCE"
    INTERN = "INTERN"
    TEMPORARY = "TEMPORARY"
    VOLUNTEER = "VOLUNTEER"
    SEASONAL = "SEASONAL"
    OTHER = "OTHER"
