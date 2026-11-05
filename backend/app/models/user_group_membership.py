from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, String, UniqueConstraint, func

from app.database.database import Base


class UserGroupMembership(Base):
    __tablename__ = "user_group_memberships"
    __table_args__ = (
        UniqueConstraint("group_id", "user_key", name="uq_group_user_key"),
    )

    id = Column(BigInteger, primary_key=True, index=True)
    group_id = Column(BigInteger, ForeignKey("user_groups.id"), nullable=False, index=True)
    # FreshKart ke end user ki pehchaan (jaise "user_123"). Admin users table se alag.
    user_key = Column(String(150), nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now())