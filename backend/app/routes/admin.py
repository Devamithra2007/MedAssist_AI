from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import (
    User,
    Prediction,
    DoctorPatientAssignment,
)
from app.schemas import (
    UserCreate,
    UserResponse,
    AdminDashboardResponse,
    AssignmentCreate,
    AssignmentResponse,
)
from app.security import hash_password

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


# ===================================================
# Verify Admin
# ===================================================

def verify_admin(current_user):
    if current_user["role"].lower() != "admin":
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )


# ===================================================
# Dashboard
# ===================================================

@router.get(
    "/dashboard",
    response_model=AdminDashboardResponse
)
def dashboard(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    verify_admin(current_user)

    total_doctors = db.query(User).filter(
        User.role.ilike("doctor")
    ).count()

    total_patients = db.query(User).filter(
        User.role.ilike("patient")
    ).count()

    total_predictions = db.query(
        Prediction
    ).count()

    total_assignments = db.query(
        DoctorPatientAssignment
    ).count()

    return AdminDashboardResponse(
        total_doctors=total_doctors,
        total_patients=total_patients,
        total_predictions=total_predictions,
        total_assignments=total_assignments,
    )


# ===================================================
# Doctors
# ===================================================

@router.get("/doctors")
def doctors(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    verify_admin(current_user)

    return db.query(User).filter(
        User.role.ilike("doctor")
    ).all()


# ===================================================
# Patients
# ===================================================

@router.get("/patients")
def patients(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    verify_admin(current_user)

    return db.query(User).filter(
        User.role.ilike("patient")
    ).all()


# ===================================================
# Create Doctor
# ===================================================

@router.post(
    "/create-doctor",
    response_model=UserResponse
)
def create_doctor(
    doctor: UserCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    verify_admin(current_user)

    existing = db.query(User).filter(
        User.email == doctor.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    new_doctor = User(
        full_name=doctor.full_name,
        email=doctor.email,
        password=hash_password(doctor.password),
        role="doctor"
    )

    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)

    return new_doctor


# ===================================================
# Delete Doctor
# ===================================================

@router.delete("/doctor/{doctor_id}")
def delete_doctor(
    doctor_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    verify_admin(current_user)

    doctor = db.query(User).filter(
        User.id == doctor_id,
        User.role.ilike("doctor")
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    db.delete(doctor)
    db.commit()

    return {
        "message": "Doctor deleted successfully"
    }


# ===================================================
# Assign Patient
# ===================================================

@router.post(
    "/assign",
    response_model=AssignmentResponse
)
def assign_patient(
    assignment: AssignmentCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    verify_admin(current_user)

    doctor = db.query(User).filter(
        User.id == assignment.doctor_id,
        User.role.ilike("doctor")
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    patient = db.query(User).filter(
        User.id == assignment.patient_id,
        User.role.ilike("patient")
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    existing = db.query(
        DoctorPatientAssignment
    ).filter(
        DoctorPatientAssignment.patient_id == assignment.patient_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Patient already assigned"
        )

    new_assignment = DoctorPatientAssignment(
        doctor_id=assignment.doctor_id,
        patient_id=assignment.patient_id,
    )

    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)

    return new_assignment   

@router.get("/assignments")
def get_assignments(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    verify_admin(current_user)

    assignments = db.query(
        DoctorPatientAssignment
    ).all()

    result = []

    for assignment in assignments:
        doctor = db.query(User).filter(
            User.id == assignment.doctor_id
        ).first()

        patient = db.query(User).filter(
            User.id == assignment.patient_id
        ).first()

        result.append({
            "id": assignment.id,
            "doctor_id": doctor.id,
            "doctor_name": doctor.full_name,
            "patient_id": patient.id,
            "patient_name": patient.full_name,
            "assigned_at": assignment.assigned_at,
        })

    return result 

@router.delete("/assignment/{assignment_id}")
def delete_assignment(
    assignment_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    verify_admin(current_user)

    assignment = db.query(
        DoctorPatientAssignment
    ).filter(
        DoctorPatientAssignment.id == assignment_id
    ).first()

    if not assignment:
        raise HTTPException(
            status_code=404,
            detail="Assignment not found"
        )

    db.delete(assignment)
    db.commit()

    return {
        "message": "Assignment deleted successfully"
    }                                           