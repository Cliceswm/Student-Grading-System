from repositories.courses_repository import get_course_by_id
from repositories.assessments_repository import get_assessment_by_id
from repositories.enrollments_repository import is_student_enrolled, get_students_for_course
from repositories.submissions_repository import (
    get_submission,
    create_or_update_submission,
    get_submissions_for_assessment,
    update_submission_grade
)
from datetime import datetime

def student_submission_service(course_id, assessment_id, student_id, form=None):
    # Check that the course exists
    course = get_course_by_id(course_id)
    if not course:
        raise ValueError("Course not found")
    
    # Check that the assessment exists
    assessment = get_assessment_by_id(assessment_id)
    if not assessment or assessment["course_id"] != course_id:
        raise ValueError("Assessment not found")

    # Check that the student is enrolled
    if not is_student_enrolled(course_id, student_id):
        raise ValueError("You are not enrolled in this course")

    # If GET → simply return the data
    if form is None:
        submission = get_submission(assessment_id, student_id)
        return course, assessment, submission

    # If POST → create/update submission
    comment = form.get("comment", "").strip()

    create_or_update_submission(assessment_id, student_id, comment)

    submission = get_submission(assessment_id, student_id)
    return course, assessment, submission


def get_teacher_submissions_service(course_id, assessment_id):
    # Check that the course exists
    course = get_course_by_id(course_id)
    if not course:
        raise ValueError("Course not found")
    
    # Check that the assessment exists
    assessment = get_assessment_by_id(assessment_id)
    if not assessment or assessment["course_id"] != course_id:
        raise ValueError("Assessment not found")

    # Get all students of the course
    students = get_students_for_course(course_id)

    # Filter only active students
    active_students = {
        s["id"]: s
        for s in students
        if s.get("role") == "student" and s.get("active") == 1
    }

    # get all submissions
    submissions = get_submissions_for_assessment(assessment_id)

    # Linking submissions to students
    result = []
    for student_id, student in active_students.items():
        sub = next((s for s in submissions if s["student_id"] == student_id), None)

        result.append({
            "student_id": student_id,
            "student_name": f"{student['first_name']} {student['last_name']}",
            "submitted": sub["submitted"] if sub else None,
            "grade": sub["grade"] if sub else None,
            "feedback": sub["feedback"] if sub else None,
        })

    return course, assessment, result


def grade_submission_service(course_id, assessment_id, student_id, form=None):
    # Validate course
    course = get_course_by_id(course_id)
    if not course:
        raise ValueError("Course not found")

    # Validate assessment
    assessment = get_assessment_by_id(assessment_id)
    if not assessment or assessment["course_id"] != course_id:
        raise ValueError("Assessment not found")

    # Validate student enrollment
    if not is_student_enrolled(course_id, student_id):
        raise ValueError("Student not enrolled in this course")

    # Load submission (may be None)
    submission = get_submission(assessment_id, student_id)

    # If no submission exists, create a virtual one for display
    if not submission:
        submission = {
            "assessment_id": assessment_id,
            "student_id": student_id,
            "submitted": None,
            "student_comment": None,
            "grade": None,
            "feedback": None,
            "lateness_days": None
        }

    # POST → update grade
    if form is not None:
        grade_raw = form.get("grade", "").strip()
        feedback = form.get("feedback", "").strip()

        # Validate grade
        if grade_raw:
            try:
                grade = float(grade_raw)
            except ValueError:
                raise ValueError("Grade must be a number")

            if grade < 0 or grade > 100:
                raise ValueError("Grade must be between 0 and 100")
        else:
            grade = None

        # Ensure submission exists in DB
        real_submission = get_submission(assessment_id, student_id)
        if real_submission is None:
            create_or_update_submission(assessment_id, student_id, comment="")

        # Now update grade
        update_submission_grade(assessment_id, student_id, grade, feedback)

        # Reload submission
        submission = get_submission(assessment_id, student_id)


    # Compute lateness_days
    if assessment["due_date"] and submission and submission["submitted"]:
        due = datetime.strptime(assessment["due_date"], "%Y-%m-%d").date()
        submitted = datetime.strptime(submission["submitted"], "%Y-%m-%d").date()
        submission["lateness_days"] = (submitted - due).days
    else:
        submission["lateness_days"] = None

    return course, assessment, submission
