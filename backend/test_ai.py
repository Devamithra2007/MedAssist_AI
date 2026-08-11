from app.ai.predict import predict_disease

result = predict_disease([
    "fever",
    "cough",
    "fatigue",
    "headache"
])

print(result)
