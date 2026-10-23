from sqlalchemy import Column, String, Float, Integer, Date, Boolean, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from app.database import Base


class BiomarkerObservation(Base):
    __tablename__ = "biomarker_observations"

    id = Column(String(64), primary_key=True)  # OBS-BIO-{CODE}-D{DAY}
    member_id = Column(String(16), ForeignKey("members.id", ondelete="CASCADE"), nullable=False)
    marker_code = Column(String(32), nullable=False)
    marker_name = Column(String(64), nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String(32), nullable=False)
    optimal_range_min = Column(Float, nullable=False)
    optimal_range_max = Column(Float, nullable=False)
    measurement_date = Column(Date, nullable=False)
    test_cycle_day = Column(Integer, nullable=False)  # 0 or 180

    member = relationship("Member", back_populates="biomarkers")

    __table_args__ = (
        Index("idx_biomarkers_member", "member_id", "measurement_date"),
    )


class WearableDailyRecord(Base):
    __tablename__ = "wearable_daily_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(String(16), ForeignKey("members.id", ondelete="CASCADE"), nullable=False)
    recorded_date = Column(Date, nullable=False)
    week_number = Column(Integer, nullable=False)  # 1 to 26
    total_sleep_hours = Column(Float, nullable=True)
    deep_sleep_hours = Column(Float, nullable=True)
    rem_sleep_hours = Column(Float, nullable=True)
    resting_heart_rate = Column(Float, nullable=True)
    hrv_rmssd = Column(Float, nullable=True)
    strain_score = Column(Float, nullable=True)
    adherence_logged = Column(Boolean, nullable=False, default=False)

    member = relationship("Member", back_populates="wearables")

    __table_args__ = (
        UniqueConstraint("member_id", "recorded_date", name="uq_member_date"),
        Index("idx_wearables_member_date", "member_id", "recorded_date"),
    )
