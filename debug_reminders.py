#!/usr/bin/env python3
"""
Debug script for testing medication reminders
Run this script to test the reminder system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, Patient, Medication, MedicationConfirmation
from datetime import datetime, time, timedelta
from scheduler import test_reminder_now, parse_timings

def main():
    app = create_app()
    
    with app.app_context():
        print("MediTracker Reminder Debug Tool")
        print("=" * 50)
        
        # List all patients
        patients = Patient.query.all()
        print(f"\nFound {len(patients)} patients:")
        for patient in patients:
            print(f"  - {patient.name} (ID: {patient.id})")
            print(f"    Email: {patient.email}")
            print(f"    Contact: {patient.contact}")
            print(f"    Caretaker: {patient.caretaker}")
        
        # List all medications
        medications = Medication.query.all()
        print(f"\nFound {len(medications)} medications:")
        for med in medications:
            patient = Patient.query.get(med.patient_id)
            print(f"  - {med.medicine} (ID: {med.id})")
            print(f"    Patient: {patient.name if patient else 'Unknown'}")
            print(f"    Dosage: {med.dosage}")
            print(f"    Timing: {med.timing}")
            print(f"    Active: {med.active}")
            
            # Parse timing
            times = parse_timings(med.timing)
            print(f"    Parsed times: {[t.strftime('%H:%M') for t in times]}")
        
        # Test a reminder
        if medications:
            print(f"\nTesting reminder for medication ID {medications[0].id}...")
            success = test_reminder_now(medications[0].id)
            if success:
                print("Test reminder sent successfully!")
            else:
                print("Failed to send test reminder")
        
        # Check recent confirmations
        recent_confirmations = MedicationConfirmation.query.filter(
            MedicationConfirmation.confirmed_at >= datetime.now() - timedelta(days=1)
        ).all()
        
        print(f"\nRecent confirmations ({len(recent_confirmations)}):")
        for conf in recent_confirmations:
            medication = Medication.query.get(conf.medication_id)
            patient = Patient.query.get(conf.patient_id)
            print(f"  - {patient.name if patient else 'Unknown'} confirmed {medication.medicine if medication else 'Unknown'} at {conf.confirmed_at}")
        
        print("\n" + "=" * 50)
        print("Debug complete!")

if __name__ == "__main__":
    main()
