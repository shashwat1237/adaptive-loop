from sqlalchemy import Column, String, Text, Date, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.database import Base


class ConfounderEvent(Base):
    __tablename__ = "confounder_events"

    id = Column(String(64), primary_key=True)  # CONF-{TYPE}-W{WEEK}
    member_id = Column(String(16), ForeignKey("members.id", ondelete="CASCADE"), nullable=False)
    event_type = Column(String(32), nullable=False)  # ILLNESS, TRAVEL, LIFE_STRESS, INJURY
    description = Column(Text, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    severity = Column(String(16), nullable=False)  # MILD, MODERATE, SEVERE

    member = relationship("Member", back_populates="confounders")

    __table_args__ = (
        Index("idx_confounders_member", "member_id", "start_date"),
    )
