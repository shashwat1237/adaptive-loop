from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Member(Base):
    __tablename__ = "members"

    id = Column(String(16), primary_key=True)  # MEM-XXXX
    full_name = Column(String(128), nullable=False)
    age = Column(Integer, nullable=False)
    biological_sex = Column(String(16), nullable=False)  # MALE, FEMALE, OTHER
    primary_goal = Column(String(256), nullable=False)
    cohort = Column(String(64), nullable=True, default="General Cohort")
    baseline_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    protocols = relationship("Protocol", back_populates="member", cascade="all, delete-orphan")
    biomarkers = relationship("BiomarkerObservation", back_populates="member", cascade="all, delete-orphan")
    wearables = relationship("WearableDailyRecord", back_populates="member", cascade="all, delete-orphan")
    confounders = relationship("ConfounderEvent", back_populates="member", cascade="all, delete-orphan")
    analyses = relationship("AnalysisRun", back_populates="member", cascade="all, delete-orphan")
