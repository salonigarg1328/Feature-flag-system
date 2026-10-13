from sqlalchemy import Column, BigInteger, Integer, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.database.database import Base


class FlagVersion(Base):
    __tablename__ = "flag_versions"
    __table_args__ = (
        UniqueConstraint("flag_id", "version_number", name="uq_flag_version"),
    )

    id = Column(BigInteger, primary_key=True, index=True)
    flag_id = Column(BigInteger, ForeignKey("flags.id"), nullable=False, index=True)
    version_number = Column(Integer, nullable=False)
    configuration = Column(JSONB, nullable=False)
    created_by = Column(BigInteger, ForeignKey("users.id"))
    created_at = Column(DateTime, server_default=func.now())

    flag = relationship("Flag")
    creator = relationship("User")