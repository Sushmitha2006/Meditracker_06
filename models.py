from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Patient(db.Model):
    __tablename__ = "patients"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    contact = db.Column(db.String(50))
    email = db.Column(db.String(120))
    history = db.Column(db.Text)
    caretaker = db.Column(db.String(120))
    password = db.Column(db.String(255))  # in demo plaintext; for real app hash it

    vitals = db.relationship("Vital", backref="patient", cascade="all, delete-orphan")
    medications = db.relationship("Medication", backref="patient", cascade="all, delete-orphan")
    medication_confirmations = db.relationship("MedicationConfirmation", backref="patient", cascade="all, delete-orphan")

class Vital(db.Model):
    __tablename__ = "vitals"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    heart_rate = db.Column(db.Integer)
    bp_systolic = db.Column(db.Integer)
    bp_diastolic = db.Column(db.Integer)
    sugar = db.Column(db.Float)
    oxygen = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Medication(db.Model):
    __tablename__ = "medications"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    medicine = db.Column(db.String(200), nullable=False)
    dosage = db.Column(db.String(50))
    timing = db.Column(db.String(100))   # e.g. "09:00,21:00" or descriptive
    duration_days = db.Column(db.Integer)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    # field to indicate if reminder active
    active = db.Column(db.Boolean, default=True)
    
    confirmations = db.relationship("MedicationConfirmation", backref="medication", cascade="all, delete-orphan")

class MedicationConfirmation(db.Model):
    __tablename__ = "medication_confirmations"
    id = db.Column(db.Integer, primary_key=True)
    medication_id = db.Column(db.Integer, db.ForeignKey("medications.id"), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    confirmed_at = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.Text)
    completed = db.Column(db.Boolean, default=True)
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)