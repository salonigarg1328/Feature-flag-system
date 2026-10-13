from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.database.database import Base


class AuditLog(Base):
    __tablename__ = "audit_log"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), index=True)
    flag_id = Column(BigInteger, ForeignKey("flags.id"), index=True)
    action = Column(String(100), nullable=False)
    before_value = Column(JSONB)
    after_value = Column(JSONB)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User")
    flag = relationship("Flag")