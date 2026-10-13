from sqlalchemy import Column, BigInteger, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import relationship
from app.database.database import Base


class UserGroupMembership(Base):
    __tablename__ = "user_group_memberships"
    __table_args__ = (
        UniqueConstraint("user_id", "group_id", name="uq_user_group"),
    )

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, index=True)
    group_id = Column(BigInteger, ForeignKey("user_groups.id"), nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User")
    group = relationship("UserGroup")