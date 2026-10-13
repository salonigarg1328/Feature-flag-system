from sqlalchemy import Column, BigInteger, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.database.database import Base


class TargetingRule(Base):
    __tablename__ = "targeting_rules"

    id = Column(BigInteger, primary_key=True, index=True)
    flag_id = Column(BigInteger, ForeignKey("flags.id"), nullable=False, index=True)
    rule_type = Column(String(50), nullable=False)
    operator = Column(String(50), nullable=False)
    attribute = Column(String(100))
    value = Column(JSONB)
    result = Column(JSONB)
    priority = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, server_default=func.now())

    flag = relationship("Flag")