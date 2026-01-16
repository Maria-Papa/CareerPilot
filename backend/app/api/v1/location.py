from app.api.deps import get_entity_or_404
from app.db import get_session
from app.models import Location
from app.schemas import LocationCreate, LocationRead, LocationUpdate
from app.services import LocationService
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/locations", tags=["locations"])

service = LocationService()
get_location_or_404 = get_entity_or_404(service.repository.get)


@router.get("", response_model=list[LocationRead])
def list_locations(
    offset: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    return service.list_locations(session, offset=offset, limit=limit)


@router.get("/{location_id}", response_model=LocationRead)
def get_location(location: Location = Depends(get_location_or_404)):
    return location


@router.post("", response_model=LocationRead, status_code=status.HTTP_201_CREATED)
def create_location(data: LocationCreate, session: Session = Depends(get_session)):
    return service.create_location(session, data)


@router.patch("/{location_id}", response_model=LocationRead)
def update_location(
    data: LocationUpdate,
    location: Location = Depends(get_location_or_404),
    session: Session = Depends(get_session),
):
    return service.update_location(session, location, data)


@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_location(
    location: Location = Depends(get_location_or_404),
    session: Session = Depends(get_session),
):
    service.delete(session, location)
    return None
