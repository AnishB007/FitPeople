from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.body_metric import MetricKind
from app.schemas.metric import MetricCreate, MetricResponse, MetricSeriesResponse
from app.schemas.profile import ProfileUpdate, ProfileResponse
from app.services import metrics as metric_service
from app.services import profile as profile_service

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me/profile", response_model=ProfileResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return profile_service.get_profile(db, current_user.id)

@router.put("/me/profile", response_model=ProfileResponse)
def update_my_profile(
    data: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated = profile_service.update_profile(db, current_user, data)
    return profile_service.get_profile(db, updated.id)

@router.post("/me/metrics", response_model=MetricResponse, status_code=201)
def log_body_metric(
    data: MetricCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return metric_service.log_metric(db, current_user.id, data)

@router.get("/me/metrics")
def get_metric_series(
    kind: MetricKind = Query(..., description="weight | resting_hr | sleep_hours | mobility"),
    range: Optional[str] = Query("12wk", description="4wk | 8wk | 12wk | 6mo"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return metric_service.get_metric_series(db, current_user.id, kind, range)