from sqlalchemy import Column, BigInteger, String, Text, DateTime, func
from app.database.database import Base


class UserGroup(Base):
    __tablename__ = "user_groups"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    created_at = Column(DateTime, server_default=func.now())