from repositories.assessments_repository import (
    get_assessment_by_id,
    get_assessments_for_course,
    add_assessment_repo, 
    assessment_title_exists,
    get_total_weight_for_course,
    update_assessment_repo
)
from repositories.courses_repository import get_course_by_id
from repositories.enrollments_repository import get_students_for_course
from repositories.submissions_repository import get_submission, get_submission_student_ids

from datetime import date, datetime


def get_assessments_service(course_id: int, user_id: int, role: str):
    course = get_course_by_id(course_id)
    if not course:
        raise ValueError("Course not found")

    assessments = get_assessments_for_course(course_id)

    # Teacher view: count submissions in X/Y format
    if role == "teacher":
        # Get all active students of the course
        active_students = get_students_for_course(course_id)
        active_ids = {s["id"] for s in active_students}
        total_students = len(active_ids)

        for a in assessments:
            submitted_ids = get_submission_student_ids(a["id"])

            # Count submissions from active students in the course.
            valid_submissions = submitted_ids & active_ids

            a["submissions_count"] = f"{len(valid_submissions)}/{total_students}"

    # Student view: grade
    else:
        for a in assessments:
            submission = get_submission(a["id"], user_id)

            if not submission:
                a["student_status"] = "Not submitted"
            elif submission["grade"] is None:
                a["student_status"] = "Not graded"
            else:
                a["student_status"] = submission["grade"]



    return course, assessments


def add_assessment_service(course_id: int, form):
    title = form.get("title", "").strip()
    description = form.get("description", "").strip()
    weight_raw = form.get("weight", "").strip()
    due_date_raw = form.get("due_date", "").strip()

    # Validate title
    if not title:
        raise ValueError("Title is required")

    # Validate weight exists
    if not weight_raw:
        raise ValueError("Weight is required")

    # Convert to float safely
    try:
        weight = float(weight_raw)
    except ValueError:
        raise ValueError("Weight must be a number")

    # Weight must be >= 0
    if weight < 0:
        raise ValueError("Weight cannot be negative")

    # Validate course exists
    course = get_course_by_id(course_id)
    if not course:
        raise ValueError("Course not found")

    # Check title uniqueness
    if assessment_title_exists(course_id, title):
        raise ValueError("An assessment with this title already exists for this course")

    # Validate due_date
    if due_date_raw:
        try:
            due_date = datetime.strptime(due_date_raw, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid date format")

        if due_date < date.today():
            raise ValueError("Due date cannot be earlier than today")
    else:
        due_date = None

    # Check remaining weight
    total_weight = get_total_weight_for_course(course_id)
    remaining_weight = 100 - total_weight

    if remaining_weight <= 0 and weight != 0:
        raise ValueError("This course already has 100% weight assigned")

    if weight > remaining_weight:
        raise ValueError(f"Weight exceeds remaining allowed weight ({remaining_weight}%)")

    # Create assessment
    new_id = add_assessment_repo(course_id, title, description, weight, due_date_raw)

    return {
        "id": new_id,
        "course_id": course_id,
        "title": title,
        "description": description,
        "weight": weight,
        "due_date": due_date_raw
    }, True


def edit_assessment_service(course_id: int, assessment_id: int, form):
    # Validate course
    course = get_course_by_id(course_id)
    if not course:
        raise ValueError("Course not found")

    # Validate assessment
    assessment = get_assessment_by_id(assessment_id)
    if not assessment or assessment["course_id"] != course_id:
        raise ValueError("Assessment not found")

    # Extract fields
    title = form.get("title", "").strip()
    description = form.get("description", "").strip()
    weight_raw = form.get("weight", "").strip()
    due_date_raw = form.get("due_date", "").strip()

    # Validate title
    if not title:
        raise ValueError("Title is required")

    # Check title uniqueness (excluding current assessment)
    if title != assessment["title"] and assessment_title_exists(course_id, title):
        raise ValueError("An assessment with this title already exists for this course")

    # Validate weight exists
    if not weight_raw:
        raise ValueError("Weight is required")

    # Convert weight
    try:
        weight = float(weight_raw)
    except ValueError:
        raise ValueError("Weight must be a number")

    if weight < 0:
        raise ValueError("Weight cannot be negative")

    # Validate due_date
    if due_date_raw:
        try:
            due_date = datetime.strptime(due_date_raw, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid date format")

        if due_date < date.today():
            raise ValueError("Due date cannot be earlier than today")
    else:
        due_date = None

    # Weight validation:
    # total weight of course minus old weight of this assessment
    total_weight = get_total_weight_for_course(course_id)
    remaining_weight = 100 - (total_weight - assessment["weight"])

    if remaining_weight <= 0 and weight != assessment["weight"]:
        raise ValueError("This course already has 100% weight assigned")

    if weight > remaining_weight:
        raise ValueError(f"Weight exceeds remaining allowed weight ({remaining_weight}%)")

    # Update assessment
    update_assessment_repo(assessment_id, title, description, weight, due_date_raw)

    return {
        "id": assessment_id,
        "course_id": course_id,
        "title": title,
        "description": description,
        "weight": weight,
        "due_date": due_date_raw
    }, True