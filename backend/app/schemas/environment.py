import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


def clean_name(value: str) -> str:
    value = value.strip()
    if len(value) < 2:
        raise ValueError("Name must be at least 2 characters")
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9 _-]*", value):
        raise ValueError(
            "Name must start with a letter and use only letters, numbers, spaces, _ or -"
        )
    return value


class EnvironmentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    description: Optional[str] = Field(default=None, max_length=500)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        return clean_name(value)


class EnvironmentUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=50)
    description: Optional[str] = Field(default=None, max_length=500)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: Optional[str]) -> Optional[str]:
        return clean_name(value) if value is not None else value


class EnvironmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None