import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.member import Member
from app.models.protocol import Protocol
from app.models.observation import BiomarkerObservation, WearableDailyRecord
from app.models.confounder import ConfounderEvent
from app.schemas.member import MemberSummaryResponse, MemberDetailResponse, MemberProfileSchema
from app.schemas.member_create import MemberCreateRequest
from app.schemas.protocol import ProtocolResponse
from app.schemas.observation import BiomarkerObservationResponse, TimelineResponse, WearableDailyRecordResponse, WeeklyRollupResponse
from app.schemas.confounder import ConfounderEventResponse
from app.engine.aggregator import DataAggregator
from app.engine.synthetic_generator import generate_member_synthetic_data

router = APIRouter()


@router.get("/members", response_model=List[MemberSummaryResponse])
def list_members(cohort: Optional[str] = None, db: Session = Depends(get_db)):
    """Lists all members, optionally filtered by cohort."""
    query = db.query(Member)
    if cohort and cohort.strip() and cohort != "All":
        query = query.filter(Member.cohort == cohort.strip())

    members = query.all()
    results = []
    for m in members:
        has_completed = any(a.status in ["COMPLETED", "ABSTAINED"] for a in m.analyses)
        results.append(MemberSummaryResponse(
            id=m.id,
            full_name=m.full_name,
            age=m.age,
            biological_sex=m.biological_sex,
            cohort=m.cohort or "General Cohort",
            primary_goal=m.primary_goal,
            baseline_notes=m.baseline_notes,
            active_protocols_count=len(m.protocols),
            has_completed_analysis=has_completed
        ))
    return results


@router.post("/members", response_model=MemberDetailResponse, status_code=status.HTTP_201_CREATED)
def create_test_member(req: MemberCreateRequest, db: Session = Depends(get_db)):
    """
    Creates a new custom test case member with a designated cohort, protocols,
    longitudinal biomarker observations, daily wearable telemetry, and confounders.
    """
    # Generate ID if not provided
    member_id = req.id
    if not member_id or not member_id.strip():
        # Find next available MEM-XXXX
        existing_ids = [m.id for m in db.query(Member.id).all()]
        seq = 2001
        while f"MEM-{seq}" in existing_ids:
            seq += 1
        member_id = f"MEM-{seq}"
    else:
        member_id = member_id.strip().upper()
        if not member_id.startswith("MEM-"):
            member_id = f"MEM-{member_id}"

        # Check duplicate
        existing = db.query(Member).filter(Member.id == member_id).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "code": "MEMBER_ALREADY_EXISTS",
                    "message": f"Member with ID '{member_id}' already exists in database.",
                    "details": {"member_id": member_id}
                }
            )

    # Create Member
    member = Member(
        id=member_id,
        full_name=req.full_name.strip(),
        age=req.age,
        biological_sex=req.biological_sex.value,
        cohort=req.cohort.strip() if req.cohort else "General Cohort",
        primary_goal=req.primary_goal.strip(),
        baseline_notes=req.baseline_notes.strip() if req.baseline_notes else None,
        created_at=datetime.datetime.utcnow()
    )
    db.add(member)
    db.flush()

    # Generate synthetic telemetry and associations
    protocols_list, biomarkers_list, wearables_list, confounders_list = generate_member_synthetic_data(
        req=req,
        member_id=member_id
    )

    for p in protocols_list:
        db.add(p)
    for b in biomarkers_list:
        db.add(b)
    for w in wearables_list:
        db.add(w)
    for c in confounders_list:
        db.add(c)

    db.commit()
    db.refresh(member)

    return MemberDetailResponse(
        member=MemberProfileSchema(
            id=member.id,
            full_name=member.full_name,
            age=member.age,
            biological_sex=member.biological_sex,
            cohort=member.cohort or "General Cohort",
            primary_goal=member.primary_goal,
            baseline_notes=member.baseline_notes
        ),
        protocols=[ProtocolResponse.model_validate(p) for p in member.protocols],
        biomarkers=[BiomarkerObservationResponse.model_validate(b) for b in member.biomarkers],
        confounders=[ConfounderEventResponse.model_validate(c) for c in member.confounders]
    )


@router.delete("/members/{member_id}", status_code=status.HTTP_200_OK)
def delete_test_member(member_id: str, db: Session = Depends(get_db)):
    """Deletes a custom test case member. Benchmark personas MEM-1001 to MEM-1003 are protected."""
    protected_members = ["MEM-1001", "MEM-1002", "MEM-1003"]
    if member_id.upper() in protected_members:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "PROTECTED_MEMBER",
                "message": f"Member '{member_id}' is a core reference benchmark persona and cannot be deleted.",
                "details": {"protected_id": member_id}
            }
        )

    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "MEMBER_NOT_FOUND",
                "message": f"Member '{member_id}' does not exist.",
                "details": {"requested_id": member_id}
            }
        )

    db.delete(member)
    db.commit()
    return {"message": f"Member '{member_id}' and all associated telemetry records were successfully deleted."}


@router.get("/members/{member_id}", response_model=MemberDetailResponse)
def get_member_detail(member_id: str, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "MEMBER_NOT_FOUND",
                "message": f"The member with identifier '{member_id}' does not exist in the database.",
                "details": {"requested_id": member_id}
            }
        )

    return MemberDetailResponse(
        member=MemberProfileSchema(
            id=member.id,
            full_name=member.full_name,
            age=member.age,
            biological_sex=member.biological_sex,
            cohort=member.cohort or "General Cohort",
            primary_goal=member.primary_goal,
            baseline_notes=member.baseline_notes
        ),
        protocols=[ProtocolResponse.model_validate(p) for p in member.protocols],
        biomarkers=[BiomarkerObservationResponse.model_validate(b) for b in member.biomarkers],
        confounders=[ConfounderEventResponse.model_validate(c) for c in member.confounders]
    )


@router.get("/members/{member_id}/timeline", response_model=TimelineResponse)
def get_member_timeline(member_id: str, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "MEMBER_NOT_FOUND",
                "message": f"The member with identifier '{member_id}' does not exist in the database.",
                "details": {"requested_id": member_id}
            }
        )

    aggregated = DataAggregator.process_longitudinal_data(
        biomarkers=member.biomarkers,
        wearables=member.wearables,
        confounders=member.confounders
    )

    daily_responses = [
        WearableDailyRecordResponse(
            recorded_date=w.recorded_date,
            week_number=w.week_number,
            total_sleep_hours=w.total_sleep_hours,
            deep_sleep_hours=w.deep_sleep_hours,
            rem_sleep_hours=w.rem_sleep_hours,
            resting_heart_rate=w.resting_heart_rate,
            hrv_rmssd=w.hrv_rmssd,
            strain_score=w.strain_score,
            adherence_logged=w.adherence_logged
        )
        for w in member.wearables
    ]

    weekly_responses = [
        WeeklyRollupResponse(**wr)
        for wr in aggregated["weekly_rollups"]
    ]

    confounder_responses = [
        ConfounderEventResponse.model_validate(c)
        for c in member.confounders
    ]

    return TimelineResponse(
        member_id=member.id,
        total_days_expected=180,
        total_days_recorded=aggregated["total_days_recorded"],
        data_completeness_rate=aggregated["data_completeness_rate"],
        protocol_adherence_rate=aggregated["protocol_adherence_rate"],
        daily_records=daily_responses,
        weekly_rollups=weekly_responses,
        confounders=confounder_responses
    )
