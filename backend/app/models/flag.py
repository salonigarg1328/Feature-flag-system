from sqlalchemy import (
    Column, BigInteger, String, Text, Boolean, DateTime,
    ForeignKey, UniqueConstraint, func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.database.database import Base


class Flag(Base):
    __tablename__ = "flags"
    __table_args__ = (
        UniqueConstraint("environment_id", "key", name="uq_flag_env_key"),
    )

    id = Column(BigInteger, primary_key=True, index=True)
    environment_id = Column(BigInteger, ForeignKey("environments.id"), nullable=False, index=True)
    key = Column(String(150), nullable=False, index=True)
    type = Column(String(50), nullable=False, default="boolean")
    default_value = Column(JSONB, nullable=False, default=False)
    enabled = Column(Boolean, nullable=False, default=False)
    description = Column(Text)
    owner_team = Column(String(100))
    created_by = Column(BigInteger, ForeignKey("users.id"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    environment = relationship("Environment", back_populates="flags")
    creator = relationship("User")