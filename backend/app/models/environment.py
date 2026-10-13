from sqlalchemy import Column, BigInteger, String, Text, DateTime, func
from sqlalchemy.orm import relationship
from app.database.database import Base


class Environment(Base):
    __tablename__ = "environments"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    flags = relationship("Flag", back_populates="environment")