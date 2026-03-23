from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, time, timedelta
from models import db, Medication, Patient, MedicationConfirmation
from utils_email import send_email
import re
import threading
import time as time_module

scheduler = BackgroundScheduler()

def parse_timings(timing_str):
    # timing_str example: "09:00,21:00" or "09:00"
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

def check_reminders():
    """Runs every minute to check for medication reminders and send alerts"""
    now = datetime.now()  # Use local time instead of UTC
    meds = Medication.query.filter_by(active=True).all()
    
    print(f"[SCHEDULER] Checking reminders at {now.strftime('%H:%M:%S')}")
    
    for med in meds:
        patient = Patient.query.get(med.patient_id)
        if not patient:
            continue
            
        times = parse_timings(med.timing)
        
        for t in times:
            # Create datetime for today with this time
            scheduled_dt = datetime.combine(now.date(), t)
            
            # If time has passed today, check for tomorrow
            if scheduled_dt <= now:
                scheduled_dt += timedelta(days=1)
            
            # Check if we're at the exact scheduled time (within 1 minute)
            time_diff = abs((now - scheduled_dt).total_seconds())
            
            if time_diff <= 60:  # Within 1 minute of scheduled time
                # Check if patient has already confirmed this medication today
                today_start = datetime.combine(now.date(), time(0, 0))
                today_end = datetime.combine(now.date(), time(23, 59))
                
                recent_confirmation = MedicationConfirmation.query.filter(
                    MedicationConfirmation.medication_id == med.id,
                    MedicationConfirmation.confirmed_at >= today_start,
                    MedicationConfirmation.confirmed_at <= today_end
                ).first()
                
                if not recent_confirmation:
                    # Send reminder notification
                    send_medication_reminder(med, patient, scheduled_dt)
                    
                    # Schedule caretaker alert for 10 minutes later
                    alert_time = scheduled_dt + timedelta(minutes=10)
                    schedule_caretaker_alert(med, patient, alert_time)

def send_medication_reminder(medication, patient, scheduled_time):
    """Send medication reminder to patient"""
    print(f"[REMINDER SENT] {patient.name} - {medication.medicine} at {scheduled_time.strftime('%H:%M')}")
    
    # In a real app, you'd trigger a frontend popup here
    # For now, we'll log it and send email if available
    subject = f"💊 Medication Reminder: {medication.medicine}"
    body = f"""
    Hi ,
    {patient.name} missed their medication
    
    Medication: {medication.medicine}
    Dosage: {medication.dosage}
    Scheduled Time: {scheduled_time.strftime('%H:%M')}
    
    Please take care of them!
    
    Best regards,
    MediTracker Team
    """
    
    # If patient has email, send email reminder
    if patient.email:
        try:
            send_email(patient.email, subject, body)
            print(f"[EMAIL SENT] Reminder email sent to {patient.email}")
        except Exception as e:
            print(f"Failed to send email reminder: {e}")

def schedule_caretaker_alert(medication, patient, alert_time):
    """Schedule a caretaker alert for 10 minutes after medication time"""
    def send_alert():
        # Wait until alert time
        time_module.sleep(600)  # 10 minutes
        
        # Check if patient confirmed in the meantime
        now = datetime.now()
        today_start = datetime.combine(now.date(), time(0, 0))
        today_end = datetime.combine(now.date(), time(23, 59))
        
        recent_confirmation = MedicationConfirmation.query.filter(
            MedicationConfirmation.medication_id == medication.id,
            MedicationConfirmation.confirmed_at >= today_start,
            MedicationConfirmation.confirmed_at <= today_end
        ).first()
        
        if not recent_confirmation:
            send_caretaker_alert(medication, patient, alert_time - timedelta(minutes=10))
    
    # Run in background thread
    thread = threading.Thread(target=send_alert)
    thread.daemon = True
    thread.start()

def send_caretaker_alert(medication, patient, scheduled_time):
    """Send alert to caretaker when patient misses medication"""
    subject = f"🚨 URGENT: {patient.name} missed {medication.medicine}"
    body = f"""
    URGENT ALERT - Medication Missed
    
    Patient: {patient.name}
    Medication: {medication.medicine} ({medication.dosage})
    Scheduled Time: {scheduled_time.strftime('%H:%M')}
    Missed At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    
    The patient has not confirmed taking their medication within 10 minutes of the scheduled time.
    Please check on them immediately and ensure they take their medication.
    
    Patient Contact: {patient.contact or 'Not provided'}
    Patient Email: {patient.email or 'Not provided'}
    
    This is an automated alert from MediTracker.
    """
    
    # Send to caretaker if available, otherwise to patient email
    recipient = patient.caretaker or patient.email or patient.contact
    if recipient:
        try:
            send_email(recipient, subject, body)
            print(f"[CARETAKER ALERT] Sent to {recipient} for {patient.name} - {medication.medicine}")
        except Exception as e:
            print(f"Failed to send caretaker alert: {e}")
    else:
        print(f"[CARETAKER ALERT] No recipient for {patient.name} - {medication.medicine}")

def test_reminder_now(medication_id):
    """Test function to trigger a reminder immediately"""
    medication = Medication.query.get(medication_id)
    if not medication:
        print(f"[ERROR] Medication with ID {medication_id} not found")
        return False
    
    patient = Patient.query.get(medication.patient_id)
    if not patient:
        print(f"[ERROR] Patient not found for medication {medication_id}")
        return False
    
    print(f"[TEST REMINDER] Triggering reminder for {patient.name} - {medication.medicine}")
    send_medication_reminder(medication, patient, datetime.now())
    return True

def trigger_reminder_for_patient(patient_id):
    """Trigger reminders for all active medications of a patient"""
    patient = Patient.query.get(patient_id)
    if not patient:
        return False
    
    medications = Medication.query.filter_by(patient_id=patient_id, active=True).all()
    if not medications:
        print(f"[INFO] No active medications found for patient {patient.name}")
        return False
    
    print(f"[TRIGGER REMINDERS] Triggering reminders for {patient.name}")
    for medication in medications:
        send_medication_reminder(medication, patient, datetime.now())
    
    return True

def cleanup_old_confirmations():
    """Clean up old confirmation records (run daily)"""
    cutoff_date = datetime.now() - timedelta(days=30)
    old_confirmations = MedicationConfirmation.query.filter(
        MedicationConfirmation.created_at < cutoff_date
    ).all()
    
    for confirmation in old_confirmations:
        db.session.delete(confirmation)
    
    if old_confirmations:
        db.session.commit()
        print(f"Cleaned up {len(old_confirmations)} old confirmation records")

# Start scheduler
def start_scheduler(app):
    # Check reminders every minute
    scheduler.add_job(
        func=lambda: with_app_context(check_reminders, app), 
        trigger="interval", 
        minutes=1, 
        id="reminder-check"
    )
    
    # Clean up old records daily at 2 AM
    scheduler.add_job(
        func=lambda: with_app_context(cleanup_old_confirmations, app),
        trigger="cron",
        hour=2,
        minute=0,
        id="cleanup-confirmations"
    )
    
    scheduler.start()
    print("Medication reminder scheduler started")

def with_app_context(func, app):
    with app.app_context():
        func()