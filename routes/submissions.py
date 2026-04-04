from flask import Blueprint, render_template, request, session
from routes.auth import role_required
from services.submissions_service import (
    student_submission_service, 
    get_teacher_submissions_service,
    grade_submission_service
)

submissions_bp = Blueprint("submissions", __name__)


# Student's submission page
@submissions_bp.route("/courses/<int:course_id>/assessments/<int:assessment_id>/submission", methods=["GET", "POST"])
@role_required("student")
def student_submission(course_id, assessment_id):
    student_id = session["user_id"]

    try:
        if request.method == "POST":
            course, assessment, submission = student_submission_service(
                course_id, assessment_id, student_id, request.form
            )
            success = "Submission saved"
        else:
            course, assessment, submission = student_submission_service(
                course_id, assessment_id, student_id
            )
            success = None

    except ValueError as e:
        return str(e), 400

    return render_template(
        "submissions/student_submission.html",
        course=course,
        assessment=assessment,
        submission=submission,
        success=success
    )


# Teacher's page with list of students' submissions
@submissions_bp.route("/courses/<int:course_id>/assessments/<int:assessment_id>/submissions")
@role_required("teacher")
def teacher_submissions(course_id, assessment_id):
    try:
        course, assessment, submissions = get_teacher_submissions_service(course_id, assessment_id)
    except ValueError as e:
        return str(e), 404

    return render_template(
        "submissions/teacher_submissions.html",
        course=course,
        assessment=assessment,
        submissions=submissions
    )


# Grading page
@submissions_bp.route("/courses/<int:course_id>/assessments/<int:assessment_id>/submissions/<int:student_id>/grade", methods=["GET", "POST"])
@role_required("teacher")
def grade_submission(course_id, assessment_id, student_id):
    try:
        if request.method == "POST":
            course, assessment, submission = grade_submission_service(
                course_id, assessment_id, student_id, request.form
            )
            success = "Grade updated"
        else:
            course, assessment, submission = grade_submission_service(
                course_id, assessment_id, student_id
            )
            success = None

    except ValueError as e:
        return str(e), 400

    return render_template(
        "submissions/grade_submission.html",
        course=course,
        assessment=assessment,
        submission=submission,
        success=success
    )