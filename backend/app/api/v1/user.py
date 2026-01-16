from typing import List

from app.api.deps import get_entity_or_404
from app.db import get_session
from app.models import User
from app.schemas import UserCreate, UserRead, UserUpdate
from app.services.user import UserService
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["users"])

service = UserService()
get_user_or_404 = get_entity_or_404(service.repository.get)
get_active_user_or_404 = get_entity_or_404(service.get_including_deleted)


@router.get("", response_model=List[UserRead])
def list_users(
    offset: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    return service.list(session, offset=offset, limit=limit)


@router.get("/{user_id}", response_model=UserRead)
def get_user(user: User = Depends(get_user_or_404)):
    return user


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(data: UserCreate, session: Session = Depends(get_session)):
    return service.create_user(session, data)


@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    data: UserUpdate,
    user: User = Depends(get_user_or_404),
    session: Session = Depends(get_session),
):
    return service.update_user(session, user, data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user: User = Depends(get_user_or_404),
    session: Session = Depends(get_session),
):
    service.delete(session, user)
    return None


@router.post("/{user_id}/restore", response_model=UserRead)
def restore_user(
    user: User = Depends(get_active_user_or_404),
    session: Session = Depends(get_session),
):
    service.restore(session, user)
    return user
