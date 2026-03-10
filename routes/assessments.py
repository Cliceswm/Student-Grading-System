from flask import Blueprint, render_template, request, session
from db import get_db
from routes.auth import login_required
from services.courses_service import get_course_by_id
from services.assessments_service import add_assessment_service, get_assessments_service

assessments_bp = Blueprint("assessments", __name__)


# Assessments page
@assessments_bp.route("/courses/<int:course_id>/assessments")
@login_required
def assessments(course_id):

    try:
        course, assessments = get_assessments_service(course_id, session["user_id"], session["role"])
    except ValueError as e:
        return str(e), 404

    return render_template(
        "assessments/assessments.html",
        course=course,
        assessments=assessments,
    )



# Add assessment page
@assessments_bp.route("/courses/<int:course_id>/assessments/add_assessment", methods=["GET", "POST"])
@login_required
def add_assessment(course_id):
    role = session["role"]

    if role != "teacher":
        return "Access denied", 403

    course = get_course_by_id(course_id)
    if not course:
        return "Course not found", 404

    error = None
    success = None

    if request.method == "POST":
        try:
            assessment, created = add_assessment_service(course_id, request.form)
            success = "Assessment created successfully"
        except ValueError as e:
            error = str(e)

    return render_template(
        "assessments/add_assessment.html",
        course=course,
        error=error,
        success=success
    )



# Stubs:
@assessments_bp.route("/courses/<int:course_id>/assessments/<int:assessment_id>/submissions")
@login_required
def assessment_submissions(course_id, assessment_id):
    return f"Teacher view for submissions of assessment {assessment_id} in course {course_id} (stub)"

@assessments_bp.route("/courses/<int:course_id>/assessments/<int:assessment_id>/submission")
@login_required
def student_submission(course_id, assessment_id):
    return f"Student view for your submission for assessment {assessment_id} in course {course_id} (stub)"
