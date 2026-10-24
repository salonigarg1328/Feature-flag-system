from datetime import datetime
from typing import Any, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

FlagType = Literal["boolean", "string", "number", "json"]


def check_default_value(flag_type: str, value: Any) -> None:
    """default_value ka type, flag ke type se match hona chahiye."""
    if flag_type == "boolean":
        ok = isinstance(value, bool)
    elif flag_type == "string":
        ok = isinstance(value, str)
    elif flag_type == "number":
        ok = isinstance(value, (int, float)) and not isinstance(value, bool)
    elif flag_type == "json":
        ok = isinstance(value, (dict, list))
    else:
        ok = False
    if not ok:
        raise ValueError(f"default_value must match the flag type '{flag_type}'")


class FlagCreate(BaseModel):
    environment_id: int = Field(gt=0)
    key: str = Field(min_length=1, max_length=150, pattern=r"^[a-z0-9_]+$")
    type: FlagType = "boolean"
    default_value: Any = False
    enabled: bool = False
    description: Optional[str] = None
    owner_team: Optional[str] = Field(default=None, max_length=100)

    @model_validator(mode="after")
    def validate_default_value(self):
        check_default_value(self.type, self.default_value)
        return self


class FlagUpdate(BaseModel):
    type: Optional[FlagType] = None
    default_value: Optional[Any] = None
    enabled: Optional[bool] = None
    description: Optional[str] = None
    owner_team: Optional[str] = Field(default=None, max_length=100)


class FlagResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    environment_id: int
    key: str
    type: str
    default_value: Any
    enabled: bool
    description: Optional[str] = None
    owner_team: Optional[str] = None
    created_by: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None