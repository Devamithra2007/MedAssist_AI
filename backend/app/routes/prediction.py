from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import User, Prediction, Symptom
from app.schemas import (
    PredictionCreate,
    PredictionUpdate,
    PredictionResponse,
    AIPredictionRequest,
)

from app.ai.predict import predict_disease

router = APIRouter(
    prefix="/prediction",
    tags=["Prediction"]
)


# =========================================================
# Create Prediction (Manual)
# =========================================================

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


# =========================================================
# Latest Prediction
# =========================================================

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
        .filter(
            Prediction.patient_id == user.id
        )
        .order_by(Prediction.created_at.desc())
        .first()
    )

    if not prediction:
        raise HTTPException(
            status_code=404,
            detail="No prediction found"
        )

    return prediction


# =========================================================
# Prediction History
# =========================================================

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
        .filter(
            Prediction.patient_id == user.id
        )
        .order_by(Prediction.created_at.desc())
        .all()
    )


# =========================================================
# Update Prediction
# =========================================================

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

    update_data = prediction_data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(prediction, key, value)

    db.commit()
    db.refresh(prediction)

    return prediction


# =========================================================
# Delete Prediction
# =========================================================

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


# =========================================================
# AI Prediction
# =========================================================

@router.post("/ai")
def ai_prediction(
    request: AIPredictionRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):

    # Logged-in user
    user = db.query(User).filter(
        User.email == current_user["sub"]
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Latest symptom record
    latest_symptom = (
        db.query(Symptom)
        .filter(
            Symptom.patient_id == user.id
        )
        .order_by(Symptom.created_at.desc())
        .first()
    )

    if not latest_symptom:
        raise HTTPException(
            status_code=404,
            detail="Please submit symptoms before requesting AI prediction."
        )

    # AI Prediction
    disease, confidence = predict_disease(
        request.symptoms
    )

    # Risk Level
    if confidence >= 90:
        risk = "High"
    elif confidence >= 70:
        risk = "Medium"
    else:
        risk = "Low"

    # Recommendation
    recommendation = (
        f"Consult a physician regarding {disease}. "
        "Follow the prescribed treatment and monitor symptoms."
    )

    # Save prediction
    prediction = Prediction(
        patient_id=user.id,
        symptom_id=latest_symptom.id,
        predicted_disease=disease,
        confidence=f"{confidence:.2f}",
        risk_level=risk,
        recommendation=recommendation,
    )

    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    return {
        "message": "Prediction generated successfully",

        "prediction_id": prediction.id,

        "disease": disease,

        "confidence": round(confidence, 2),

        "risk_level": risk,

        "recommendation": recommendation,

        "created_at": prediction.created_at,
    }