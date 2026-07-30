from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_current_user
from app.database import get_db
from app.models import User, PatientProfile
from app.schemas import (
    PatientProfileCreate,
    PatientProfileUpdate,
    PatientProfileResponse,
)

router = APIRouter(
    prefix="/patient",
    tags=["Patient"]
)


@router.get("/dashboard")
def patient_dashboard(current_user=Depends(get_current_user)):
    if current_user["role"].lower() != "patient":
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    return {
        "message": f"Welcome {current_user['sub']}!"
    }


@router.post(
    "/profile",
    response_model=PatientProfileResponse
)
def create_profile(
    profile: PatientProfileCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):

    user = db.query(User).filter(
        User.email == current_user["sub"]
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    existing = db.query(PatientProfile).filter(
        PatientProfile.user_id == user.id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Profile already exists"
        )

    new_profile = PatientProfile(
        user_id=user.id,
        **profile.model_dump()
    )

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return new_profile


@router.get(
    "/profile",
    response_model=PatientProfileResponse
)
def get_profile(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):

    user = db.query(User).filter(
        User.email == current_user["sub"]
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    profile = db.query(PatientProfile).filter(
        PatientProfile.user_id == user.id
    ).first()

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    return profile


@router.put(
    "/profile",
    response_model=PatientProfileResponse
)
def update_profile(
    profile_data: PatientProfileUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):

    user = db.query(User).filter(
        User.email == current_user["sub"]
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    profile = db.query(PatientProfile).filter(
        PatientProfile.user_id == user.id
    ).first()

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    update_data = profile_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(profile, key, value)

    db.commit()
    db.refresh(profile)

    return profile