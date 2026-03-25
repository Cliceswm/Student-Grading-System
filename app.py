from flask import Flask
from routes.auth import auth_bp
from routes.profile import profile_bp
from routes.courses import courses_bp
from routes.users import users_bp
from routes.enrollments import enrollments_bp
from routes.assessments import assessments_bp
from routes.submissions import submissions_bp
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()

from db import close_db

def create_app():
    app = Flask(__name__)
    
    app.secret_key = "supersecretkey"

    csrf.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(enrollments_bp)
    app.register_blueprint(assessments_bp)
    app.register_blueprint(submissions_bp)

    # Register DB teardown
    app.teardown_appcontext(close_db)

    return app



# Open browser with localhost
import webbrowser
import threading

def open_browser():
    webbrowser.open("http://127.0.0.1:5000")


if __name__ == "__main__":
    threading.Timer(1, open_browser).start()
    app = create_app()
    app.run(debug=True, use_reloader=False)
