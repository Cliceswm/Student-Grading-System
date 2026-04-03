from flask import Blueprint, render_template, request, redirect, url_for, session, abort
from functools import wraps
from db import get_db
from services.auth_service import authenticate_user

auth_bp = Blueprint("auth", __name__)

# Decorator @role_required
def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if "user_id" not in session:
                return redirect(url_for("auth.login"))

            if "role" not in session or session["role"] not in roles:
                return redirect(url_for("auth.login")) # Change later

            return f(*args, **kwargs)
        return wrapper
    return decorator



# Global context processor automatically passing current_user to all templates
@auth_bp.app_context_processor
def inject_user():
    user = None
    if "user_id" in session:
        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE id = ?", 
            (session["user_id"],)
        ).fetchone()
    return dict(current_user=user)


# Login page
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        identifier = request.form["identifier"]
        password = request.form["password"]

        user, error = authenticate_user(identifier, password)

        if error:
            return render_template("login.html", error=error)

        # Successful login
        session["user_id"] = user["id"]
        session["role"] = user["role"]

        return redirect(url_for("courses.courses"))

    return render_template("login.html")


# Logout
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
