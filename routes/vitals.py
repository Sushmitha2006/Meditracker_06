from flask import Blueprint, request, jsonify
from models import db, Vital, Patient

vitals_bp = Blueprint("vitals", __name__)

@vitals_bp.route("/add", methods=["POST"])
def add_vital():
    data = request.json
    required = ["patient_id"]
    if not data.get("patient_id"):
        return jsonify({"error": "patient_id required"}), 400
    v = Vital(
        patient_id=data["patient_id"],
        heart_rate=data.get("heart_rate"),
        bp_systolic=data.get("bp_systolic"),
        bp_diastolic=data.get("bp_diastolic"),
        sugar=data.get("sugar"),
        oxygen=data.get("oxygen")
    )
    db.session.add(v)
    db.session.commit()
    return jsonify({"message": "vital recorded", "id": v.id})

@vitals_bp.route("/all/<int:patient_id>", methods=["GET"])
def get_all(patient_id):
    vs = Vital.query.filter_by(patient_id=patient_id).order_by(Vital.timestamp.asc()).all()
    out = []
    for v in vs:
        out.append({
            "id": v.id,
            "heart_rate": v.heart_rate,
            "bp_systolic": v.bp_systolic,
            "bp_diastolic": v.bp_diastolic,
            "sugar": v.sugar,
            "oxygen": v.oxygen,
            "timestamp": v.timestamp.isoformat()
        })
    return jsonify(out)
