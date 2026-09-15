from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
import enum
from datetime import datetime, timezone

class MetricKind(str, enum.Enum):
    weight       = "weight"
    resting_hr   = "resting_hr"
    sleep_hours  = "sleep_hours"
    mobility     = "mobility"

class BodyMetric(Base):
    __tablename__ = "body_metrics"

    id          = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id     = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    kind        = Column(Enum(MetricKind), nullable=False)
    value       = Column(Numeric(6, 2), nullable=False)
    unit        = Column(String, nullable=False)
    notes       = Column(String, nullable=True)
    recorded_at = Column(DateTime(timezone=True), nullable=False,
                         default=lambda: datetime.now(timezone.utc))

    # Relationship back to User — like @ManyToOne in JPA
    user = relationship("User", back_populates="body_metrics")