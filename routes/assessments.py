from flask import Blueprint, render_template, redirect, url_for, request, session
from db import get_db
from routes.auth import role_required
from services.courses_service import get_course_by_id
from services.assessments_service import (
    add_assessment_service, 
    get_assessments_service,
    get_assessment_by_id,
    edit_assessment_service
)

assessments_bp = Blueprint("assessments", __name__)


# Assessments page
@assessments_bp.route("/courses/<int:course_id>/assessments")
@role_required("teacher", "student")
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
@role_required("teacher")
def add_assessment(course_id):
    course = get_course_by_id(course_id)
    if not course:
        return "Course not found", 404

    error = None

    if request.method == "POST":
        try:
            add_assessment_service(course_id, request.form)
            return redirect(url_for("assessments.assessments", course_id=course_id))
        except ValueError as e:
            error = str(e)

    return render_template(
        "assessments/add_assessment.html",
        course=course,
        error=error,
    )


# Edit assessment page
@assessments_bp.route("/courses/<int:course_id>/assessments/<int:assessment_id>/edit", methods=["GET", "POST"])
@role_required("teacher")
def edit_assessment(course_id, assessment_id):
    assessment = get_assessment_by_id(assessment_id)
    if not assessment or assessment["course_id"] != course_id:
        return "Assessment not found", 404

    course = get_course_by_id(course_id)

    if request.method == "POST":
        try:
            updated, success = edit_assessment_service(course_id, assessment_id, request.form)
            assessment = updated
        except ValueError as e:
            return render_template(
                "assessments/edit_assessment.html",
                course=course,
                assessment=assessment,
                error=str(e)
            )

        return render_template(
            "assessments/edit_assessment.html",
            course=course,
            assessment=assessment,
            success="Assessment updated successfully"
        )

    return render_template(
        "assessments/edit_assessment.html",
        course=course,
        assessment=assessment
    )