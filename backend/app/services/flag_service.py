from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.environment import Environment
from app.models.flag import Flag
from app.models.user import User
from app.schemas.flag import FlagCreate, FlagUpdate, check_default_value


def get_flag_or_404(db: Session, flag_id: int) -> Flag:
    flag = db.get(Flag, flag_id)
    if flag is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Flag not found")
    return flag


def list_flags(db: Session, environment_id: Optional[int] = None) -> list[Flag]:
    query = db.query(Flag)
    if environment_id is not None:
        query = query.filter(Flag.environment_id == environment_id)
    return query.order_by(Flag.id).all()


def create_flag(db: Session, data: FlagCreate, user: User) -> Flag:
    if db.get(Environment, data.environment_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Environment not found")

    duplicate = (
        db.query(Flag)
        .filter(Flag.environment_id == data.environment_id, Flag.key == data.key)
        .first()
    )
    if duplicate:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "A flag with this key already exists in this environment",
        )

    flag = Flag(**data.model_dump(), created_by=user.id)
    db.add(flag)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "A flag with this key already exists in this environment",
        )
    db.refresh(flag)
    return flag


def update_flag(db: Session, flag_id: int, data: FlagUpdate) -> Flag:
    flag = get_flag_or_404(db, flag_id)

    changes = data.model_dump(exclude_unset=True)
    # sirf description aur owner_team ko khaali (None) kiya ja sakta hai
    changes = {
        k: v for k, v in changes.items()
        if v is not None or k in ("description", "owner_team")
    }

    new_type = changes.get("type", flag.type)
    new_default = changes.get("default_value", flag.default_value)
    try:
        check_default_value(new_type, new_default)
    except ValueError as exc:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc))

    for field, value in changes.items():
        setattr(flag, field, value)
    flag.updated_at = func.now()

    db.commit()
    db.refresh(flag)
    return flag


def delete_flag(db: Session, flag_id: int) -> None:
    flag = get_flag_or_404(db, flag_id)
    db.delete(flag)
    db.commit()