from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.analysis import AnalysisRun
from app.models.member import Member
from app.schemas.analysis import AnalysisCreateRequest, AnalysisRunResponse
from app.engine.coordinator import AdaptiveLoopCoordinator

router = APIRouter()


@router.post("/analyses", response_model=AnalysisRunResponse, status_code=status.HTTP_201_CREATED)
def trigger_analysis(request: AnalysisCreateRequest, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.id == request.member_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "MEMBER_NOT_FOUND",
                "message": f"The member with identifier '{request.member_id}' does not exist in the database.",
                "details": {"requested_id": request.member_id}
            }
        )

    try:
        result = AdaptiveLoopCoordinator.run_analysis(
            member_id=request.member_id,
            db=db,
            force_recompute=request.force_recompute
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": "INTERNAL_ENGINE_ERROR",
                "message": str(e),
                "details": {"member_id": request.member_id}
            }
        )


@router.get("/analyses/{analysis_id}", response_model=AnalysisRunResponse)
def get_analysis_by_id(analysis_id: str, db: Session = Depends(get_db)):
    analysis = db.query(AnalysisRun).filter(AnalysisRun.id == analysis_id).first()
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "ANALYSIS_NOT_FOUND",
                "message": f"The analysis run with identifier '{analysis_id}' does not exist.",
                "details": {"requested_id": analysis_id}
            }
        )

    return AnalysisRunResponse.model_validate(analysis)


@router.get("/members/{member_id}/analyses/latest", response_model=AnalysisRunResponse)
def get_latest_member_analysis(member_id: str, db: Session = Depends(get_db)):
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

    latest = (
        db.query(AnalysisRun)
        .filter(AnalysisRun.member_id == member_id)
        .order_by(AnalysisRun.triggered_at.desc())
        .first()
    )
    if not latest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "ANALYSIS_NOT_FOUND",
                "message": f"No analysis runs found for member '{member_id}'.",
                "details": {"requested_id": member_id}
            }
        )

    return AnalysisRunResponse.model_validate(latest)
