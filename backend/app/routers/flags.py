from typing import Optional

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.database import get_db
from app.models.user import User
from app.schemas.flag import FlagCreate, FlagResponse, FlagUpdate
from app.services import flag_service

router = APIRouter(prefix="/api/v1/flags", tags=["Flags"])


@router.post("", response_model=FlagResponse, status_code=status.HTTP_201_CREATED)
def create_flag(
    data: FlagCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return flag_service.create_flag(db, data, current_user)


@router.get("", response_model=list[FlagResponse])
def list_flags(
    environment_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return flag_service.list_flags(db, environment_id)


@router.get("/{flag_id}", response_model=FlagResponse)
def get_flag(
    flag_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return flag_service.get_flag_or_404(db, flag_id)


@router.put("/{flag_id}", response_model=FlagResponse)
def update_flag(
    flag_id: int,
    data: FlagUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return flag_service.update_flag(db, flag_id, data)


@router.delete("/{flag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_flag(
    flag_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    flag_service.delete_flag(db, flag_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)