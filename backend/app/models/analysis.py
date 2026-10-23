from sqlalchemy import Column, String, Float, DateTime, JSON, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class AnalysisRun(Base):
    __tablename__ = "analysis_runs"

    id = Column(String(64), primary_key=True)  # ANL-{UUID}
    member_id = Column(String(16), ForeignKey("members.id", ondelete="CASCADE"), nullable=False)
    triggered_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(String(32), nullable=False)  # PENDING, PROCESSING, COMPLETED, FAILED, ABSTAINED
    final_action = Column(String(64), nullable=True)  # 5 canonical actions
    critic_verdict = Column(String(16), nullable=True)  # APPROVED, AMENDED, REJECTED
    data_completeness_rate = Column(Float, nullable=False, default=0.0)
    protocol_adherence_rate = Column(Float, nullable=False, default=0.0)
    input_summary_snapshot = Column(JSON, nullable=False)
    analyst_payload = Column(JSON, nullable=True)
    verification_payload = Column(JSON, nullable=True)
    critic_payload = Column(JSON, nullable=True)

    member = relationship("Member", back_populates="analyses")

    __table_args__ = (
        Index("idx_analyses_member", "member_id", "triggered_at"),
    )
