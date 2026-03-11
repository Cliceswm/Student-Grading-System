from repositories.assessments_repository import add_assessment_repo
from repositories.courses_repository import get_course_by_id

from repositories.assessments_repository import (
    get_assessments_for_course,
    add_assessment_repo, 
    assessment_title_exists)
from repositories.courses_repository import get_course_by_id


def get_assessments_service(course_id: int, user_id: int, role: str):
    course = get_course_by_id(course_id)
    if not course:
        raise ValueError("Course not found")

    assessments = get_assessments_for_course(course_id)

    # stubs:
    for a in assessments:
        if role == "teacher":
            a["submissions_count"] = 0   # stub
        else:
            a["final_grade"] = None      # stub

    return course, assessments


from datetime import date, datetime
from repositories.assessments_repository import (
    add_assessment_repo,
    assessment_title_exists,
    get_total_weight_for_course
)
from repositories.courses_repository import get_course_by_id


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

    if remaining_weight <= 0:
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