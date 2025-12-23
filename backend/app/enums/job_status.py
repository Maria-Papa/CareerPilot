from enum import StrEnum, unique


@unique
class JobStatus(StrEnum):
    DRAFT = "DRAFT"
    SAVED = "SAVED"
    APPLIED = "APPLIED"
    INTERVIEW = "INTERVIEW"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN"
    OFFER = "OFFER"
