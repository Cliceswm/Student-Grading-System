from repositories.courses_repository import (
    fetch_all_courses_for_admin,
    fetch_courses_for_teacher,
    fetch_courses_for_student,
    insert_course,
    get_course_by_id,
    update_course
)
from repositories.users_repository import get_user_by_id, get_all_teachers
from repositories.assessments_repository import get_assessments_for_course
from repositories.submissions_repository import get_submission
from services.enrollments_service import count_active_students_for_course


def get_courses_for_user(role: str, user_id: int):
    if role == "admin":
        courses = fetch_all_courses_for_admin()

    elif role == "teacher":
        courses = fetch_courses_for_teacher(user_id)

    else:  # student
        courses = fetch_courses_for_student(user_id)

    enriched = []

    for c in courses:
        course = dict(c)

        if role in ("admin", "teacher"):
            count, _ = count_active_students_for_course(course["id"])
            course["active_students"] = count
            course["final_grade"] = None

        else:  # student
            course["active_students"] = None
            final = compute_final_grade_for_student(course["id"], user_id)
            course["final_grade"] = final

        enriched.append(course)

    return enriched



def add_course(name: str):
    success, error = insert_course(name)

    if not success:
        return None, error

    return "Course added", None


def load_course_for_edit(course_id: int):
    return get_course_by_id(course_id)


def load_teachers_for_course_edit():
    teachers = get_all_teachers()
    return [t for t in teachers if t["active"]
]


def process_course_edit(course_id: int, form):
    name = form["name"].strip()

    # Normalize teacher_id
    teacher_id_raw = form.get("teacher_id")

    if teacher_id_raw is None or teacher_id_raw.strip() == "":
        teacher_id = None
    else:
        # Checking if a value is a number
        if not teacher_id_raw.isdigit():
            raise ValueError("Wrong teacher id")

        teacher_id = int(teacher_id_raw)

    # Load current course
    current = get_course_by_id(course_id)
    if not current:
        raise ValueError("Course not found")

    # Validate teacher
    if teacher_id is not None:
        teacher = get_user_by_id(teacher_id)

        # 1) There is no such user
        if not teacher:
            raise ValueError("Teacher with such id does not exist")

        # 2) User is not a teacher
        if teacher["role"] != "teacher":
            raise ValueError("Cannot assign a user, who is not a teacher")

        # 3) Teacher is not active
        if not teacher["active"]:
            raise ValueError("Cannot assign an inactive teacher")

    # Check if data changed
    no_changes = (
        current["name"] == name and
        current["teacher_id"] == teacher_id
    )

    if no_changes:
        return current, False

    # Apply update
    update_course(course_id, name, teacher_id)

    updated = get_course_by_id(course_id)
    return updated, True


def compute_final_grade_for_student(course_id, student_id):
    assessments = get_assessments_for_course(course_id)

    total = None

    for a in assessments:
        submission = get_submission(a["id"], student_id)

        # Ignore if not submitted
        if not submission:
            continue

        # Ignore if submitted but not graded
        if submission["grade"] is None:
            continue

        # Ignore if assessment weight <= 0
        if a["weight"] <= 0:
            continue

        # Add weighted grade
        if total is None:
            total = submission["grade"] * (a["weight"] / 100)
        else:
            total += submission["grade"] * (a["weight"] / 100)

    # If nothing graded yet → return None
    return round(total, 2) if total is not None else None
