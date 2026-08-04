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

    user = db.query(User).filter(User.id == patient_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    profile = db.query(PatientProfile).filter(
        PatientProfile.user_id == patient_id
    ).first()

    return {
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "role": user.role,

        "phone": profile.phone if profile else None,
        "date_of_birth": profile.date_of_birth if profile else None,
        "gender": profile.gender if profile else None,
        "blood_group": profile.blood_group if profile else None,
        "height": profile.height if profile else None,
        "weight": profile.weight if profile else None,
        "address": profile.address if profile else None,
        "emergency_contact": profile.emergency_contact if profile else None,
        "allergies": profile.allergies if profile else None,
        "medical_history": profile.medical_history if profile else None,
    }

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

@router.get("/summary")
def doctor_summary(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    verify_doctor(current_user)

    total_patients = db.query(User).filter(
        User.role == "Patient"
    ).count()

    total_predictions = db.query(Prediction).count()

    total_reports = db.query(PatientProfile).count()

    high_risk = db.query(Prediction).filter(
        Prediction.risk_level == "High"
    ).count()

    return {
        "total_patients": total_patients,
        "total_predictions": total_predictions,
        "total_reports": total_reports,
        "high_risk_patients": high_risk
    }