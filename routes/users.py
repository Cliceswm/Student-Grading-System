from flask import Blueprint, render_template, request, redirect, url_for
from routes.auth import login_required, admin_required
from services.users_service import (
    get_all_users,
    create_user,
    get_user_by_id,
    admin_update_user
)

users_bp = Blueprint("users", __name__)


# Users page (admin only)
@users_bp.route("/users")
@login_required
@admin_required
def manage_users():
    users = get_all_users()
    return render_template("users.html", users=users)


# Add a user page (admin only)
@users_bp.route("/users/add_user", methods=["GET", "POST"])
@login_required
@admin_required
def add_user():
    if request.method == "POST":
        first_name = request.form["first_name"].strip()
        last_name = request.form["last_name"].strip()
        email = request.form["email"].lower().strip()
        password = request.form["password"]
        role = request.form["role"]

        success, error = create_user(first_name, last_name, email, password, role)

        if error:
            return render_template(
                "users/add_user.html",
                error=error,
                first_name=first_name,
                last_name=last_name,
                email=email,
                role=role
            )

        return redirect("/users")

    return render_template("users/add_user.html")


# Edit user page (admin only)
@users_bp.route("/users/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_user(user_id):
    user = get_user_by_id(user_id)

    if not user:
        return "User not found", 404

    error = None
    success = None

    if request.method == "POST":
        first_name = request.form["first_name"].strip()
        last_name = request.form["last_name"].strip()
        email = request.form["email"].lower().strip()
        role = request.form["role"]
        active = int(request.form["status"])
        new_password = request.form.get("new_password", "").strip()

        success, error = admin_update_user(
            user_id,
            first_name,
            last_name,
            email,
            role,
            active,
            new_password
        )

        if success:
            user = get_user_by_id(user_id)

    return render_template(
        "users/edit_user.html",
        user=user,
        error=error,
        success=success
    )
