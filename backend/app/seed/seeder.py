import logging
from sqlalchemy.orm import Session
from app.database import engine, Base, SessionLocal
from app.models import (
    Member,
    Protocol,
    BiomarkerObservation,
    WearableDailyRecord,
    ConfounderEvent,
    AnalysisRun
)
from app.seed.persona_clean import get_marcus_vance_data
from app.seed.persona_confounded import get_elena_rostova_data
from app.seed.persona_nonadherent import get_david_chen_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seed_database(db: Session):
    logger.info("Initializing database tables...")
    Base.metadata.create_all(bind=engine)

    personas = [
        get_marcus_vance_data(),
        get_elena_rostova_data(),
        get_david_chen_data()
    ]

    for p in personas:
        m_data = p["member"]
        existing = db.query(Member).filter(Member.id == m_data["id"]).first()
        if existing:
            logger.info(f"Member {m_data['id']} already exists. Skipping.")
            continue

        logger.info(f"Seeding member {m_data['id']} ({m_data['full_name']})...")
        member = Member(
            id=m_data["id"],
            full_name=m_data["full_name"],
            age=m_data["age"],
            biological_sex=m_data["biological_sex"],
            cohort=m_data.get("cohort", "General Cohort"),
            primary_goal=m_data["primary_goal"],
            baseline_notes=m_data["baseline_notes"]
        )
        db.add(member)
        db.flush()

        # Add protocols
        for prot in p["protocols"]:
            db.add(Protocol(
                id=prot["id"],
                member_id=member.id,
                name=prot["name"],
                category=prot["category"],
                dosage_or_frequency=prot["dosage_or_frequency"],
                start_date=prot["start_date"],
                review_date=prot["review_date"],
                target_adherence_rate=prot["target_adherence_rate"]
            ))

        # Add biomarkers
        for bio in p["biomarkers"]:
            db.add(BiomarkerObservation(
                id=bio["id"],
                member_id=member.id,
                marker_code=bio["marker_code"],
                marker_name=bio["marker_name"],
                value=bio["value"],
                unit=bio["unit"],
                optimal_range_min=bio["optimal_range_min"],
                optimal_range_max=bio["optimal_range_max"],
                measurement_date=bio["measurement_date"],
                test_cycle_day=bio["test_cycle_day"]
            ))

        # Add confounders
        for conf in p["confounders"]:
            db.add(ConfounderEvent(
                id=conf["id"],
                member_id=member.id,
                event_type=conf["event_type"],
                description=conf["description"],
                start_date=conf["start_date"],
                end_date=conf["end_date"],
                severity=conf["severity"]
            ))

        # Add wearables
        for w in p["wearables"]:
            db.add(WearableDailyRecord(
                member_id=member.id,
                recorded_date=w["recorded_date"],
                week_number=w["week_number"],
                total_sleep_hours=w["total_sleep_hours"],
                deep_sleep_hours=w["deep_sleep_hours"],
                rem_sleep_hours=w["rem_sleep_hours"],
                resting_heart_rate=w["resting_heart_rate"],
                hrv_rmssd=w["hrv_rmssd"],
                strain_score=w["strain_score"],
                adherence_logged=w["adherence_logged"]
            ))

        db.commit()
        logger.info(f"Successfully seeded member {m_data['id']}.")

    logger.info("Database seeding complete!")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
