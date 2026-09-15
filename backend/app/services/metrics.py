from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi import HTTPException
from datetime import datetime, timezone, timedelta
from app.models.body_metric import BodyMetric, MetricKind
from app.schemas.metric import MetricCreate

# Maps range string to number of days
RANGE_DAYS = {
    "4wk":  28,
    "8wk":  56,
    "12wk": 84,
    "6mo":  180,
}

def log_metric(db: Session, user_id: str, data: MetricCreate) -> BodyMetric:
    recorded_at = data.recorded_at or datetime.now(timezone.utc)

    metric = BodyMetric(
        user_id=user_id,
        kind=data.kind,
        value=data.value,
        unit=data.unit,
        notes=data.notes,
        recorded_at=recorded_at,
    )
    db.add(metric)
    db.commit()
    db.refresh(metric)
    return metric

def get_metric_series(
    db: Session,
    user_id: str,
    kind: MetricKind,
    range_str: str = "12wk"
) -> dict:
    days = RANGE_DAYS.get(range_str, 84)
    since = datetime.now(timezone.utc) - timedelta(days=days)

    # Query metrics for this user, kind, in date range, ordered by date
    metrics = db.query(BodyMetric).filter(
        BodyMetric.user_id == user_id,
        BodyMetric.kind == kind,
        BodyMetric.recorded_at >= since
    ).order_by(BodyMetric.recorded_at.asc()).all()

    if not metrics:
        return {
            "kind": kind.value,
            "unit": _default_unit(kind),
            "data": [],
            "latest": None,
            "change": None,
        }

    data_points = [
        {
            "date": m.recorded_at.strftime("%Y-%m-%d"),
            "value": float(m.value)
        }
        for m in metrics
    ]

    latest = float(metrics[-1].value)
    change = round(float(metrics[-1].value) - float(metrics[0].value), 2)

    return {
        "kind": kind.value,
        "unit": metrics[0].unit,
        "data": data_points,
        "latest": latest,
        "change": change,
    }

def _default_unit(kind: MetricKind) -> str:
    defaults = {
        MetricKind.weight: "kg",
        MetricKind.resting_hr: "bpm",
        MetricKind.sleep_hours: "hrs",
        MetricKind.mobility: "score",
    }
    return defaults.get(kind, "")