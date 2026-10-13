from sqlalchemy import Column, BigInteger, Integer, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database.database import Base


class EvaluationStat(Base):
    __tablename__ = "evaluation_stats"
    __table_args__ = (
        UniqueConstraint("flag_id", "environment_id", "date", "hour", name="uq_eval_stat"),
    )

    id = Column(BigInteger, primary_key=True, index=True)
    flag_id = Column(BigInteger, ForeignKey("flags.id"), nullable=False, index=True)
    environment_id = Column(BigInteger, ForeignKey("environments.id"), nullable=False, index=True)
    date = Column(Date, nullable=False)
    hour = Column(Integer, nullable=False)
    evaluation_count = Column(BigInteger, nullable=False, default=0)

    flag = relationship("Flag")
    environment = relationship("Environment")