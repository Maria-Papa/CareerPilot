from app.schemas import ORMBase


class JobTagBase(ORMBase):
    job_id: int
    tag_id: int


class JobTagCreate(ORMBase):
    tag_id: int


class JobTagUpdate(ORMBase):
    tag_id: int | None = None


class JobTagRead(JobTagBase):
    class Config:
        from_attributes = True
