from app.api.deps import get_entity_or_404
from app.db import get_session
from app.models import File
from app.schemas import FileCreate, FileRead, FileUpdate
from app.services.file import FileService
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/files", tags=["files"])

service = FileService()
get_file_or_404 = get_entity_or_404(service.repository.get)
get_active_file_or_404 = get_entity_or_404(service.get_including_deleted)


@router.get("", response_model=list[FileRead])
def list_files(
    offset: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    return service.list(session, offset=offset, limit=limit)


@router.get("/{file_id}", response_model=FileRead)
def get_file(file: File = Depends(get_file_or_404)):
    return file


@router.post("", response_model=FileRead, status_code=status.HTTP_201_CREATED)
def create_file(data: FileCreate, session: Session = Depends(get_session)):
    return service.create_file(session, data)


@router.patch("/{file_id}", response_model=FileRead)
def update_file(
    data: FileUpdate,
    file: File = Depends(get_file_or_404),
    session: Session = Depends(get_session),
):
    return service.update_file(session, file, data)


@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_file(
    file: File = Depends(get_file_or_404),
    session: Session = Depends(get_session),
):
    service.delete(session, file)
    return None


@router.post("/{file_id}/restore", response_model=FileRead)
def restore_file(
    file: File = Depends(get_active_file_or_404),
    session: Session = Depends(get_session),
):
    service.restore(session, file)
    return file
