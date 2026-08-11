import pandas as pd
import joblib

from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.preprocessing import LabelEncoder

from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)

# ==========================
# Load Dataset
# ==========================

df = pd.read_csv("D:\MedAssist_AI\datasets\dataset.csv")

df = df.fillna("None")

# ==========================
# Feature Engineering
# ==========================

symptom_columns = [
    col for col in df.columns
    if col.startswith("Symptom")
]

symptom_lists = df[symptom_columns].values.tolist()

symptom_lists = [
    [
        symptom.strip().lower()
        for symptom in row
        if symptom != "None"
    ]
    for row in symptom_lists
]

mlb = MultiLabelBinarizer()

X = mlb.fit_transform(symptom_lists)

# ==========================
# Encode Disease Labels
# ==========================

label_encoder = LabelEncoder()

y = label_encoder.fit_transform(df["Disease"])

# ==========================
# Train/Test Split
# ==========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

# ==========================
# Train Model
# ==========================

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
)

model.fit(X_train, y_train)

# ==========================
# Prediction
# ==========================

predictions = model.predict(X_test)

# ==========================
# Evaluation
# ==========================

accuracy = accuracy_score(
    y_test,
    predictions,
)

print("=" * 60)
print("Accuracy")
print(f"{accuracy * 100:.2f}%")

print("=" * 60)
print("Classification Report")

print(
    classification_report(
        y_test,
        predictions,
        target_names=label_encoder.classes_,
    )
)

print("=" * 60)
print("Confusion Matrix")

print(confusion_matrix(y_test, predictions))

# ==========================
# Save Model
# ==========================

joblib.dump(
    model,
    "../models/model.pkl"
)

joblib.dump(
    label_encoder,
    "../models/label_encoder.pkl"
)

joblib.dump(
    mlb,
    "../models/mlb.pkl"
)

print("=" * 60)
print("Model Saved Successfully!")