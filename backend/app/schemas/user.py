from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRegister(BaseModel):
    """Registration ke time user jo bhejega."""
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)


class UserLogin(BaseModel):
    """Login ke time user jo bhejega."""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """User ka data jo wapas bhejenge (password kabhi nahi)."""
    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    """Login ke baad jo token dete hain."""
    access_token: str
    token_type: str = "bearer"