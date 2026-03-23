from flask import Blueprint, request, jsonify
from models import db, Medication, Patient

medication_bp = Blueprint("medication", __name__)

@medication_bp.route("/add", methods=["POST"])
def add_med():
    data = request.json
    required = ["patient_id", "medicine"]
    if not data.get("patient_id") or not data.get("medicine"):
        return jsonify({"error": "patient_id and medicine required"}), 400
    
    med = Medication(
        patient_id=data["patient_id"],
        medicine=data["medicine"],
        dosage=data.get("dosage"),
        timing=data.get("timing"),  # example: "09:00,21:00"
        duration_days=data.get("duration_days", 30),
        active=data.get("active", True)
    )
    db.session.add(med)
    db.session.commit()
    return jsonify({"message": "medication added", "id": med.id})

@medication_bp.route("/list/<int:patient_id>", methods=["GET"])
def list_meds(patient_id):
    meds = Medication.query.filter_by(patient_id=patient_id).all()
    out = []
    for m in meds:
        out.append({
            "id": m.id,
            "medicine": m.medicine,
            "dosage": m.dosage,
            "timing": m.timing,
            "duration_days": m.duration_days,
            "active": m.active
        })
    return jsonify(out)

@medication_bp.route("/toggle/<int:med_id>", methods=["PUT"])
def toggle_medication(med_id):
    data = request.json
    med = Medication.query.get(med_id)
    if not med:
        return jsonify({"error": "medication not found"}), 404
    
    med.active = data.get("active", not med.active)
    db.session.commit()
    return jsonify({"message": "medication status updated", "active": med.active})

@medication_bp.route("/delete/<int:med_id>", methods=["DELETE"])
def delete_medication(med_id):
    med = Medication.query.get(med_id)
    if not med:
        return jsonify({"error": "medication not found"}), 404
    
    db.session.delete(med)
    db.session.commit()
    return jsonify({"message": "medication deleted"})

@medication_bp.route("/deactivate/<int:med_id>", methods=["POST"])
def deactivate(med_id):
    med = Medication.query.get(med_id)
    if not med:
        return jsonify({"error": "not found"}), 404
    med.active = False
    db.session.commit()
    return jsonify({"message": "deactivated"})