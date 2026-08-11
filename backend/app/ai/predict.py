import numpy as np
from pathlib import Path
import joblib


# Base directory
BASE_DIR = Path(__file__).resolve().parent

MODEL = joblib.load(BASE_DIR / "models" / "model.pkl")
LABEL_ENCODER = joblib.load(BASE_DIR / "models" / "label_encoder.pkl")
MLB = joblib.load(BASE_DIR / "models" / "mlb.pkl")

def predict_disease(symptoms: list[str]):

    cleaned = [
        symptom.strip().lower()
        for symptom in symptoms
        if symptom.strip()
    ]

    X = MLB.transform([cleaned])

    prediction = MODEL.predict(X)[0]

    probabilities = MODEL.predict_proba(X)[0]

    confidence = float(np.max(probabilities) * 100)

    disease = LABEL_ENCODER.inverse_transform(
        [prediction]
    )[0]

    return disease, confidence