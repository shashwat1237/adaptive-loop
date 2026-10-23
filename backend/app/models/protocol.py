from sqlalchemy import Column, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Protocol(Base):
    __tablename__ = "protocols"

    id = Column(String(32), primary_key=True)  # PROT-CATEGORY-XX
    member_id = Column(String(16), ForeignKey("members.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(128), nullable=False)
    category = Column(String(32), nullable=False)  # LIFESTYLE, SUPPLEMENT, EXERCISE, NUTRITION
    dosage_or_frequency = Column(String(128), nullable=False)
    start_date = Column(Date, nullable=False)
    review_date = Column(Date, nullable=False)
    target_adherence_rate = Column(Float, nullable=False, default=80.0)

    member = relationship("Member", back_populates="protocols")
