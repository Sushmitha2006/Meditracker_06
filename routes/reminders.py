from flask import Blueprint, request, jsonify
from models import db, Medication, Patient, MedicationConfirmation
from datetime import datetime, timedelta
from utils_email import send_email
import re

reminders_bp = Blueprint("reminders", __name__)

@reminders_bp.route("/health-check", methods=["GET"])
def health():
    return jsonify({"status": "ok", "msg": "reminders service up"})

@reminders_bp.route("/test/<int:medication_id>", methods=["POST"])
def test_reminder(medication_id):
    """Test endpoint to trigger a reminder immediately"""
    from scheduler import test_reminder_now
    
    success = test_reminder_now(medication_id)
    if success:
        return jsonify({"message": "Test reminder sent successfully"})
    else:
        return jsonify({"error": "Failed to send test reminder"}), 400

@reminders_bp.route("/trigger-all/<int:patient_id>", methods=["POST"])
def trigger_all_reminders(patient_id):
    """Trigger all reminders for a patient"""
    from scheduler import trigger_reminder_for_patient
    
    success = trigger_reminder_for_patient(patient_id)
    if success:
        return jsonify({"message": "All reminders triggered successfully"})
    else:
        return jsonify({"error": "Failed to trigger reminders"}), 400

@reminders_bp.route("/trigger-popup/<int:patient_id>", methods=["POST"])
def trigger_popup(patient_id):
    """Trigger a popup notification for a patient"""
    data = request.json
    medication_id = data.get("medication_id")
    
    if not medication_id:
        return jsonify({"error": "medication_id required"}), 400
    
    medication = Medication.query.get(medication_id)
    if not medication or medication.patient_id != patient_id:
        return jsonify({"error": "Medication not found or doesn't belong to patient"}), 404
    
    # In a real app, you'd use WebSockets or Server-Sent Events here
    # For now, we'll just return the medication data for the frontend to show
    return jsonify({
        "message": "Popup triggered",
        "medication": {
            "id": medication.id,
            "medicine": medication.medicine,
            "dosage": medication.dosage,
            "timing": medication.timing
        }
    })

@reminders_bp.route("/confirm", methods=["POST"])
def confirm_medication():
    """Record that a patient has confirmed taking their medication"""
    data = request.json
    required_fields = ["medication_id", "patient_id", "confirmed_at"]
    
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Check if medication exists and belongs to patient
    medication = Medication.query.get(data["medication_id"])
    if not medication or medication.patient_id != data["patient_id"]:
        return jsonify({"error": "Medication not found or doesn't belong to patient"}), 404
    
    # Create confirmation record
    confirmation = MedicationConfirmation(
        medication_id=data["medication_id"],
        patient_id=data["patient_id"],
        confirmed_at=datetime.fromisoformat(data["confirmed_at"].replace('Z', '+00:00')),
        notes=data.get("notes", "")
    )
    
    db.session.add(confirmation)
    db.session.commit()
    
    return jsonify({"message": "Medication confirmation recorded", "id": confirmation.id})

@reminders_bp.route("/caretaker-alert", methods=["POST"])
def send_caretaker_alert():
    """Send alert to caretaker when patient misses medication"""
    data = request.json
    required_fields = ["patient_id", "medication_id", "medication_name", "dosage", "timing"]
    
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Get patient information
    patient = Patient.query.get(data["patient_id"])
    if not patient:
        return jsonify({"error": "Patient not found"}), 404
    
    # Prepare alert message
    subject = f"🚨 Medication Alert: {patient.name} missed {data['medication_name']}"
    body = f"""
    ALERT: Medication Reminder Missed
    
    Patient: {patient.name}
    Medication: {data['medication_name']} ({data['dosage']})
    Scheduled Time: {data['timing']}
    Missed At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    
    Please check on the patient and ensure they take their medication.
    
    Patient Contact: {patient.contact or 'Not provided'}
    Patient Email: {patient.email or 'Not provided'}
    
    This is an automated alert from MediTracker.
    """
    
    # Send to caretaker if available, otherwise to patient
    recipient = patient.caretaker or patient.email or patient.contact
    if recipient:
        try:
            send_email(recipient, subject, body)
            return jsonify({"message": "Caretaker alert sent successfully"})
        except Exception as e:
            return jsonify({"error": f"Failed to send alert: {str(e)}"}), 500
    else:
        return jsonify({"error": "No caretaker contact information available"}), 400

@reminders_bp.route("/upcoming/<int:patient_id>", methods=["GET"])
def get_upcoming_reminders(patient_id):
    """Get upcoming medication reminders for a patient"""
    now = datetime.now()
    upcoming_reminders = []
    
    # Get active medications for the patient
    medications = Medication.query.filter_by(patient_id=patient_id, active=True).all()
    
    for med in medications:
        times = parse_timings(med.timing)
        for time_obj in times:
            # Create datetime for today with this time
            reminder_time = datetime.combine(now.date(), time_obj)
            
            # If time has passed today, check for tomorrow
            if reminder_time <= now:
                reminder_time += timedelta(days=1)
            
            # Check if there's a recent confirmation for this medication
            recent_confirmation = MedicationConfirmation.query.filter(
                MedicationConfirmation.medication_id == med.id,
                MedicationConfirmation.confirmed_at >= reminder_time - timedelta(hours=1),
                MedicationConfirmation.confirmed_at <= reminder_time + timedelta(hours=1)
            ).first()
            
            if not recent_confirmation:
                upcoming_reminders.append({
                    "medication_id": med.id,
                    "medicine": med.medicine,
                    "dosage": med.dosage,
                    "timing": med.timing,
                    "reminder_time": reminder_time.isoformat(),
                    "is_overdue": reminder_time < now
                })
    
    return jsonify(upcoming_reminders)

@reminders_bp.route("/completed/<int:reminder_id>", methods=["POST"])
def mark_reminder_completed(reminder_id):
    """Mark a reminder as completed (alternative to confirm endpoint)"""
    data = request.json
    confirmation = MedicationConfirmation.query.get(reminder_id)
    
    if not confirmation:
        return jsonify({"error": "Reminder not found"}), 404
    
    confirmation.completed = True
    confirmation.completed_at = datetime.now()
    db.session.commit()
    
    return jsonify({"message": "Reminder marked as completed"})

def parse_timings(timing_str):
    """Parse timing string into time objects"""
    if not timing_str:
        return []
    parts = re.split(r'[;,]\s*', timing_str)
    times = []
    for p in parts:
        try:
            h, m = map(int, p.strip().split(":"))
            times.append(time(hour=h, minute=m))
        except:
            continue
    return times