from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import User, PatientProfile, Symptom, Prediction

router = APIRouter(
    prefix="/doctor",
    tags=["Doctor"]
)


def verify_doctor(current_user):
    if current_user["role"].lower() != "doctor":
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )


@router.get("/dashboard")
def doctor_dashboard(
    current_user=Depends(get_current_user)
):
    verify_doctor(current_user)

    return {
        "message": f"Welcome Dr. {current_user['sub']}"
    }


@router.get("/patients")
def get_patients(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    verify_doctor(current_user)

    return db.query(User).filter(
        User.role == "Patient"
    ).all()


@router.get("/patient/{patient_id}")
def patient_profile(
    patient_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    verify_doctor(current_user)

    profile = db.query(PatientProfile).filter(
        PatientProfile.user_id == patient_id
    ).first()

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return profile


@router.get("/patient/{patient_id}/symptoms")
def patient_symptoms(
    patient_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    verify_doctor(current_user)

    return db.query(Symptom).filter(
        Symptom.patient_id == patient_id
    ).all()


@router.get("/patient/{patient_id}/predictions")
def patient_predictions(
    patient_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    verify_doctor(current_user)

    return db.query(Prediction).filter(
        Prediction.patient_id == patient_id
    ).all()