from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False)

    password = Column(String, nullable=False)

    role = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # One user -> One patient profile
    patient_profile = relationship(
        "PatientProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )


class PatientProfile(Base):
    __tablename__ = "patient_profiles"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=False,
    )

    phone = Column(String(20))
    date_of_birth = Column(String(20))
    gender = Column(String(20))
    blood_group = Column(String(10))

    height = Column(String(10))
    weight = Column(String(10))

    address = Column(Text)

    emergency_contact = Column(String(20))

    allergies = Column(Text)

    medical_history = Column(Text)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    user = relationship(
        "User",
        back_populates="patient_profile",
    )
class Symptom(Base):
    __tablename__ = "symptoms"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    fever = Column(String(20))
    cough = Column(String(20))
    headache = Column(String(20))
    fatigue = Column(String(20))
    chest_pain = Column(String(20))
    shortness_of_breath = Column(String(20))

    blood_pressure = Column(String(20))
    heart_rate = Column(String(20))
    blood_sugar = Column(String(20))
    temperature = Column(String(20))

    notes = Column(Text)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    patient = relationship("User")

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    symptom_id = Column(
        Integer,
        ForeignKey("symptoms.id"),
        nullable=False
    )

    predicted_disease = Column(String(100))

    confidence = Column(String(20))

    risk_level = Column(String(20))

    recommendation = Column(Text)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    patient = relationship("User")
    symptom = relationship("Symptom")