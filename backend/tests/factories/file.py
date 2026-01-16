from app.enums.file_type import FileType
from app.models.file import File
from sqlalchemy.orm import Session


def create_file(db_session: Session, **kwargs) -> File:
    if "user_id" not in kwargs:
        raise ValueError("file_factory requires user_id")

    file = File(
        user_id=kwargs["user_id"],
        file_url=kwargs.get("file_url", "http://example.com/file.pdf"),
        file_type=kwargs.get("file_type", FileType.CV),
    )
    db_session.add(file)
    db_session.commit()
    db_session.refresh(file)
    return file
