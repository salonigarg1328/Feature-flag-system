from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.environment import Environment
from app.models.flag import Flag
from app.schemas.environment import EnvironmentCreate, EnvironmentUpdate
from app.services import flag_service


def get_environment_or_404(db: Session, environment_id: int) -> Environment:
    env = db.get(Environment, environment_id)
    if env is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Environment not found")
    return env


def list_environments(db: Session) -> list[Environment]:
    return db.query(Environment).order_by(Environment.id).all()


def _name_taken(db: Session, name: str, exclude_id: Optional[int] = None) -> bool:
    query = db.query(Environment).filter(func.lower(Environment.name) == name.lower())
    if exclude_id is not None:
        query = query.filter(Environment.id != exclude_id)
    return query.first() is not None


def create_environment(db: Session, data: EnvironmentCreate) -> Environment:
    if _name_taken(db, data.name):
        raise HTTPException(
            status.HTTP_409_CONFLICT, "An environment with this name already exists"
        )
    env = Environment(**data.model_dump())
    db.add(env)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT, "An environment with this name already exists"
        )
    db.refresh(env)
    return env


def update_environment(
    db: Session, environment_id: int, data: EnvironmentUpdate
) -> Environment:
    env = get_environment_or_404(db, environment_id)

    changes = data.model_dump(exclude_unset=True)
    # name khaali nahi ho sakta, description ko khaali (None) kiya ja sakta hai
    changes = {k: v for k, v in changes.items() if v is not None or k == "description"}

    new_name = changes.get("name")
    if new_name and _name_taken(db, new_name, exclude_id=env.id):
        raise HTTPException(
            status.HTTP_409_CONFLICT, "An environment with this name already exists"
        )

    for field, value in changes.items():
        setattr(env, field, value)
    db.commit()
    db.refresh(env)
    return env


def delete_environment(db: Session, environment_id: int) -> None:
    env = get_environment_or_404(db, environment_id)

    flag_count = db.query(Flag).filter(Flag.environment_id == environment_id).count()
    if flag_count:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            f"Cannot delete: {flag_count} flag(s) still use this environment. "
            "Delete or move them first.",
        )

    db.delete(env)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "Cannot delete: this environment is still referenced by other records",
        )


def list_environment_flags(db: Session, environment_id: int) -> list[Flag]:
    get_environment_or_404(db, environment_id)
    return flag_service.list_flags(db, environment_id)