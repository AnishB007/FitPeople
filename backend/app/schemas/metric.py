from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from app.models.body_metric import MetricKind

class MetricCreate(BaseModel):
    kind: MetricKind
    value: float = Field(..., gt=0, description="Must be positive")
    unit: str = Field(..., min_length=1, max_length=20)
    notes: Optional[str] = None
    recorded_at: Optional[datetime] = None  # defaults to now if not sent

class MetricResponse(BaseModel):
    id: UUID
    kind: MetricKind
    value: float
    unit: str
    notes: Optional[str]
    recorded_at: datetime

    class Config:
        from_attributes = True

class MetricSeriesResponse(BaseModel):
    kind: str
    unit: str
    data: List[dict]           # [{ "date": "2026-09-01", "value": 72.5 }]
    latest: Optional[float]    # most recent value
    change: Optional[float]    # change from first to last in range