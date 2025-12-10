from sqlalchemy import Column, Integer, String, Date, Float, Text
from sqlalchemy.sql import func
from .database import Base


class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)

    company = Column(String, index=True)
    position_title = Column(String, index=True)
    position_generalized = Column(String, index=True)

    url = Column(String)

    location = Column(String)
    expected_salary = Column(Float, nullable=True)
    given_salary = Column(Float, nullable=True)

    flexibility = Column(String)  # on-site, hybrid, remote
    status = Column(
        String, index=True
    )  # applied, saved, rejected, no-response, declined

    application_date = Column(Date, nullable=True)
    rejection_date = Column(Date, nullable=True)
    saved_date = Column(Date, nullable=True)
    declined_date = Column(Date, nullable=True)

    rejected_reason = Column(Text, nullable=True)

    cv_path = Column(String, nullable=True)
    cover_letter_path = Column(String, nullable=True)

    notes = Column(Text, nullable=True)

    created_at = Column(Date, server_default=func.now())
