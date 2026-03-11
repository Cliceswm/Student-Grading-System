from flask import Blueprint, render_template, request, redirect, url_for, session
from routes.auth import login_required, admin_required
from services.courses_service import get_courses_for_user, add_course
from services.enrollments_service import count_active_students_for_course

courses_bp = Blueprint("courses", __name__)


# Main route. Leads to courses/ if logged in, otherwise to login/
@courses_bp.route("/")
@login_required
def index():
    return redirect(url_for("courses.courses"))


# Courses page
@courses_bp.route("/courses")
@login_required
def courses():
    role = session["role"]
    user_id = session["user_id"]

    courses = get_courses_for_user(role, user_id)

    return render_template("courses.html", courses=courses)


# Add a course page
@courses_bp.route("/courses/add_course", methods=["GET", "POST"])
@login_required
@admin_required
def add_course_route():

    if request.method == "POST":
        name = request.form["name"]

        success, error = add_course(name)

        if error:
            return render_template(
                "courses/add_course.html",
                error=error,
                name=name
            )

        return redirect(url_for("courses.courses"))

    return render_template("courses/add_course.html")


# Edit course page
@courses_bp.route("/courses/<int:course_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_course(course_id):
    from services.courses_service import (
        load_course_for_edit,
        load_teachers_for_course_edit,
        process_course_edit
    )

    error = None
    success = None

    try:
        course = load_course_for_edit(course_id)
    except ValueError as e:
        return str(e), 404

    if request.method == "POST":
        try:
            course, changed = process_course_edit(course_id, request.form)
            if changed:
                success = "Course updated successfully"
        except ValueError as e:
            error = str(e)

    teachers = load_teachers_for_course_edit()

    active_enroled, error = count_active_students_for_course(course_id)

    return render_template(
        "courses/edit_course.html",
        course=course,
        teachers=teachers,
        active_enroled=active_enroled,
        error=error,
        success=success
    )