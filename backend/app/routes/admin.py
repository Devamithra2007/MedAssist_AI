from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import User
from app.schemas import UserCreate, UserResponse
from app.security import hash_password

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


def verify_admin(current_user):
    if current_user["role"].lower() != "admin":
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )


@router.get("/dashboard")
def dashboard(current_user=Depends(get_current_user)):
    verify_admin(current_user)

    return {
        "message": f"Welcome Admin {current_user['sub']}"
    }


@router.get("/doctors")
def doctors(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    verify_admin(current_user)

    return db.query(User).filter(
        User.role == "Doctor"
    ).all()


@router.get("/patients")
def patients(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    verify_admin(current_user)

    return db.query(User).filter(
        User.role == "Patient"
    ).all()


@router.post("/create-doctor", response_model=UserResponse)
def create_doctor(
    doctor: UserCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
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
        role="Doctor"
    )

    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)

    return new_doctor


@router.delete("/doctor/{doctor_id}")
def delete_doctor(
    doctor_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    verify_admin(current_user)

    doctor = db.query(User).filter(
        User.id == doctor_id,
        User.role == "Doctor"
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