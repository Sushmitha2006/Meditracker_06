from pydantic import BaseModel, Field
from typing import Optional, List

class PatientIn(BaseModel):
    name: str
    age: Optional[int]
    gender: Optional[str]
    contact: Optional[str]
    email: Optional[str]
    history: Optional[str]
    caretaker: Optional[str]
    password: Optional[str]

class VitalIn(BaseModel):
    patient_id: int
    heart_rate: Optional[int]
    bp_systolic: Optional[int]
    bp_diastolic: Optional[int]
    sugar: Optional[float]
    oxygen: Optional[float]

class MedicationIn(BaseModel):
    patient_id: int
    medicine: str
    dosage: Optional[str]
    timing: Optional[str]
    duration_days: Optional[int] = Field(default=30)
