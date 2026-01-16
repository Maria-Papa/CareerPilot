from typing import Sequence

from app.api.deps import get_entity_or_404, get_session
from app.models import Tag
from app.schemas.tag import TagCreate, TagRead, TagUpdate
from app.services.tag import TagService
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/tags", tags=["tags"])

service = TagService()
get_tag_or_404 = get_entity_or_404(service.repository.get)


@router.get("/", response_model=list[TagRead])
def list_tags(
    offset: int = 0, limit: int = 100, session: Session = Depends(get_session)
) -> Sequence[Tag]:
    return service.list_tags(session, offset=offset, limit=limit)


@router.get("/{tag_id}", response_model=TagRead)
def get_tag(tag: Tag = Depends(get_tag_or_404)) -> Tag:
    return tag


@router.post("/", response_model=TagRead, status_code=status.HTTP_201_CREATED)
def create_tag(data: TagCreate, session: Session = Depends(get_session)) -> Tag:
    return service.create_tag(session, data)


@router.patch("/{tag_id}", response_model=TagRead)
def update_tag(
    data: TagUpdate,
    tag: Tag = Depends(get_tag_or_404),
    session: Session = Depends(get_session),
) -> Tag:
    return service.update_tag(session, tag, data)


@router.delete(
    "/{tag_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_tag(
    tag: Tag = Depends(get_tag_or_404),
    session: Session = Depends(get_session),
) -> None:
    service.delete_tag(session, tag)
