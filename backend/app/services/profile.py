from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.profile import ProfileUpdate

def get_profile(db: Session, user_id: str) -> dict:
    user = db.query(User).filter(User.id == user_id).first()

    # Count total metrics logged
    from app.models.body_metric import BodyMetric
    metric_count = db.query(BodyMetric).filter(
        BodyMetric.user_id == user_id
    ).count()

    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role.value,
        "avatar_initials": user.avatar_initials,
        "created_at": user.created_at,
        "total_metrics_logged": metric_count,
    }

def update_profile(db: Session, user: User, data: ProfileUpdate) -> User:
    if data.full_name is not None:
        user.full_name = data.full_name
        # Regenerate initials if name changed
        parts = data.full_name.strip().split()
        user.avatar_initials = (parts[0][0] + parts[-1][0]).upper() \
                               if len(parts) > 1 else parts[0][:2].upper()

    if data.avatar_initials is not None:
        user.avatar_initials = data.avatar_initials.upper()

    db.commit()
    db.refresh(user)
    return user