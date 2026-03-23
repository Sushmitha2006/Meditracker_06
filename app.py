from flask import Flask
from flask_cors import CORS
from config import Config
from models import db
from routes.auth import auth_bp
from routes.vitals import vitals_bp
from routes.medication import medication_bp
from routes.reminders import reminders_bp
from scheduler import start_scheduler

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    db.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(vitals_bp, url_prefix="/api/vitals")
    app.register_blueprint(medication_bp, url_prefix="/api/medication")
    app.register_blueprint(reminders_bp, url_prefix="/api/reminders")

    @app.route("/")
    def index():
        return {"message": "MediTracker API running"}

    with app.app_context():
        # create tables
        db.create_all()

    # start reminder scheduler
    start_scheduler(app)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
