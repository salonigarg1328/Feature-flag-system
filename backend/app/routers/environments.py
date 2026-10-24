from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.database import get_db
from app.models.user import User
from app.schemas.environment import (
    EnvironmentCreate,
    EnvironmentResponse,
    EnvironmentUpdate,
)
from app.schemas.flag import FlagResponse
from app.services import environment_service

router = APIRouter(prefix="/api/v1/environments", tags=["Environments"])


@router.post(
    "", response_model=EnvironmentResponse, status_code=status.HTTP_201_CREATED
)
def create_environment(
    data: EnvironmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return environment_service.create_environment(db, data)


@router.get("", response_model=list[EnvironmentResponse])
def list_environments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return environment_service.list_environments(db)


@router.get("/{environment_id}", response_model=EnvironmentResponse)
def get_environment(
    environment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return environment_service.get_environment_or_404(db, environment_id)


@router.put("/{environment_id}", response_model=EnvironmentResponse)
def update_environment(
    environment_id: int,
    data: EnvironmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return environment_service.update_environment(db, environment_id, data)


@router.delete("/{environment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_environment(
    environment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    environment_service.delete_environment(db, environment_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{environment_id}/flags", response_model=list[FlagResponse])
def list_environment_flags(
    environment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return environment_service.list_environment_flags(db, environment_id)