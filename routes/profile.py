from flask import Blueprint, render_template, request, session
from db import get_db
from routes.auth import role_required
from services.profile_service import update_email, change_password

profile_bp = Blueprint("profile", __name__)


# Profile page
@profile_bp.route("/profile", methods=["GET", "POST"])
@role_required("admin", "teacher", "student")
def profile():
    db = get_db()
    user_id = session["user_id"]

    user = db.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()

    error = None
    success = None
    show_email_form = False
    show_password_form = False

    if request.method == "POST" and "show_email_form" in request.form:
        show_email_form = True

    if request.method == "POST" and "show_password_form" in request.form:
        show_password_form = True

    if request.method == "POST" and "update_email" in request.form:
        show_email_form = True
        new_email = request.form["email"].lower().strip()

        success, error = update_email(user_id, new_email)

        if success:
            show_email_form = False
            user = db.execute(
                "SELECT * FROM users WHERE id = ?",
                (user_id,)
            ).fetchone()

    if request.method == "POST" and "change_password" in request.form:
        show_password_form = True

        old_password = request.form["old_password"]
        new_password = request.form["new_password"]
        repeat_password = request.form["repeat_password"]

        success, error = change_password(user, old_password, new_password, repeat_password)

        if success:
            show_password_form = False

    return render_template(
        "profile.html",
        error=error,
        success=success,
        show_password_form=show_password_form,
        show_email_form=show_email_form
    )