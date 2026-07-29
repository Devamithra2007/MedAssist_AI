from fastapi import FastAPI

from app.database import engine
from app import models
from app.routes.auth import router as auth_router
from app.routes.patient import router as patient_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MedAssist-AI API",
    version="1.0.0"
)

# Include Authentication Routes
app.include_router(auth_router)
app.include_router(patient_router)

@app.get("/")
def home():
    return {
        "message": "Database Connected Successfully!"
    }