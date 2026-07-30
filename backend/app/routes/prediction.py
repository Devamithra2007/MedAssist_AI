from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import User, Prediction
from app.schemas import (
    PredictionCreate,
    PredictionUpdate,
    PredictionResponse,
)

router = APIRouter(
    prefix="/prediction",
    tags=["Prediction"]
)


@router.post("/", response_model=PredictionResponse)
def create_prediction(
    prediction: PredictionCreate,
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

    new_prediction = Prediction(
        patient_id=user.id,
        **prediction.model_dump()
    )

    db.add(new_prediction)
    db.commit()
    db.refresh(new_prediction)

    return new_prediction


@router.get("/", response_model=PredictionResponse)
def get_latest_prediction(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):

    user = db.query(User).filter(
        User.email == current_user["sub"]
    ).first()

    prediction = (
        db.query(Prediction)
        .filter(Prediction.patient_id == user.id)
        .order_by(Prediction.created_at.desc())
        .first()
    )

    if not prediction:
        raise HTTPException(
            status_code=404,
            detail="No prediction found"
        )

    return prediction


@router.get("/history", response_model=list[PredictionResponse])
def prediction_history(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):

    user = db.query(User).filter(
        User.email == current_user["sub"]
    ).first()

    return (
        db.query(Prediction)
        .filter(Prediction.patient_id == user.id)
        .order_by(Prediction.created_at.desc())
        .all()
    )


@router.put("/{prediction_id}", response_model=PredictionResponse)
def update_prediction(
    prediction_id: int,
    prediction_data: PredictionUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):

    user = db.query(User).filter(
        User.email == current_user["sub"]
    ).first()

    prediction = (
        db.query(Prediction)
        .filter(
            Prediction.id == prediction_id,
            Prediction.patient_id == user.id
        )
        .first()
    )

    if not prediction:
        raise HTTPException(
            status_code=404,
            detail="Prediction not found"
        )

    update_data = prediction_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(prediction, key, value)

    db.commit()
    db.refresh(prediction)

    return prediction


@router.delete("/{prediction_id}")
def delete_prediction(
    prediction_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):

    user = db.query(User).filter(
        User.email == current_user["sub"]
    ).first()

    prediction = (
        db.query(Prediction)
        .filter(
            Prediction.id == prediction_id,
            Prediction.patient_id == user.id
        )
        .first()
    )

    if not prediction:
        raise HTTPException(
            status_code=404,
            detail="Prediction not found"
        )

    db.delete(prediction)
    db.commit()

    return {
        "message": "Prediction deleted successfully"
    }