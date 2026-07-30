from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import User, PatientProfile, Symptom, Prediction

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/profile")
def profile_report(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(
        User.email == current_user["sub"]
    ).first()

    profile = db.query(PatientProfile).filter(
        PatientProfile.user_id == user.id
    ).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return profile


@router.get("/symptoms")
def symptoms_report(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(
        User.email == current_user["sub"]
    ).first()

    return db.query(Symptom).filter(
        Symptom.patient_id == user.id
    ).all()


@router.get("/predictions")
def predictions_report(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(
        User.email == current_user["sub"]
    ).first()

    return db.query(Prediction).filter(
        Prediction.patient_id == user.id
    ).all()


@router.get("/summary")
def summary_report(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(
        User.email == current_user["sub"]
    ).first()

    profile = db.query(PatientProfile).filter(
        PatientProfile.user_id == user.id
    ).first()

    symptoms = db.query(Symptom).filter(
        Symptom.patient_id == user.id
    ).all()

    predictions = db.query(Prediction).filter(
        Prediction.patient_id == user.id
    ).all()

    return {
        "profile": profile,
        "symptoms": symptoms,
        "predictions": predictions
    }