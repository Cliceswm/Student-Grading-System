from services.users_service import get_user_by_id, get_all_users
from services.courses_service import get_course_by_id
from repositories.enrollments_repository import (
    get_students_for_course,
    enroll_student as enroll_student_repo,
    unenroll_student as unenroll_student_repo
)


def load_enrollment_data(course_id):
    course = get_course_by_id(course_id)
    if not course:
        return None, None, "Course not found"

    all_users = get_all_users()
    students = [u for u in all_users if u["role"] == "student"]

    enrolled = get_students_for_course(course_id)
    enrolled_ids = {s["id"] for s in enrolled}

    return students, enrolled_ids, None


def enroll_student(course_id, student_id_raw):
    if student_id_raw is None or str(student_id_raw).strip() == "":
        return None, None

    if not str(student_id_raw).isdigit():
        return None, "Invalid student ID"

    student_id = int(student_id_raw)

    course = get_course_by_id(course_id)
    if not course:
        return None, "Course not found"

    student = get_user_by_id(student_id)
    if not student:
        return None, "User not found"

    if student["role"] != "student":
        return None, "Only students can be enrolled"

    if not student["active"]:
        return None, "Cannot enroll an inactive student"

    enrolled = get_students_for_course(course_id)
    enrolled_ids = {s["id"] for s in enrolled}

    if student_id in enrolled_ids:
        return None, "Student is already enrolled"

    enroll_student_repo(course_id, student_id)
    return f"Student {student_id:05d} - {student['last_name']} {student['first_name']} enrolled", None



def unenroll_student(course_id, student_id):
    student_id = int(student_id)

    course = get_course_by_id(course_id)
    if not course:
        return None, "Course not found"

    student = get_user_by_id(student_id)
    if not student:
        return None, "User not found"

    enrolled = get_students_for_course(course_id)
    enrolled_ids = {s["id"] for s in enrolled}

    if student_id not in enrolled_ids:
        return None, "Student is not enrolled"


    unenroll_student_repo(course_id, student_id)
    return f"Student {student_id:05d} - {student["last_name"]} {student["first_name"]} was unenrolled", None


def count_active_students_for_course(course_id):
    course = get_course_by_id(course_id)
    if not course:
        return None, "Course not found"

    enrolled = get_students_for_course(course_id)

    active_students = [s for s in enrolled if s["active"]]

    return len(active_students), None
