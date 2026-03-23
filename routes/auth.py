from flask import Blueprint, request, jsonify, current_app
from models import db, Patient

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    if not data.get("name") or not data.get("password"):
        return jsonify({"error": "name and password required"}), 400
    p = Patient(
        name=data.get("name"),
        age=data.get("age"),
        gender=data.get("gender"),
        contact=data.get("contact"),
        email=data.get("email"),
        history=data.get("history"),
        caretaker=data.get("caretaker"),
        password=data.get("password")  # demo only: do hashing in prod
    )
    db.session.add(p)
    db.session.commit()
    return jsonify({"message": "registered", "patient_id": p.id})

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    name = data.get("name")
    password = data.get("password")
    p = Patient.query.filter_by(name=name, password=password).first()
    if not p:
        return jsonify({"error": "invalid credentials"}), 401
    return jsonify({
        "message": "ok",
        "patient": {
            "id": p.id, "name": p.name, "age": p.age, "gender": p.gender,
            "contact": p.contact, "email": p.email, "caretaker": p.caretaker
        }
    })
