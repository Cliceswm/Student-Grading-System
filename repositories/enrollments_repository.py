from db import get_db

def get_students_for_course(course_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT u.id, u.first_name, u.last_name, u.email, u.role, u.active
        FROM enrollments e
        JOIN users u ON u.id = e.student_id
        WHERE e.course_id = ?
          AND u.role = 'student'
          AND u.active = 1
    """, (course_id,))

    return [dict(row) for row in cursor.fetchall()]


def enroll_student(course_id, student_id):
    db = get_db()
    db.execute("""
        INSERT OR IGNORE INTO enrollments (course_id, student_id)
        VALUES (?, ?)
    """, (course_id, student_id))
    db.commit()


def unenroll_student(course_id, student_id):
    db = get_db()
    db.execute("""
        DELETE FROM enrollments
        WHERE course_id = ? AND student_id = ?
    """, (course_id, student_id))
    db.commit()


def is_student_enrolled(course_id, student_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT 1
        FROM enrollments
        WHERE course_id = ? AND student_id = ?
        LIMIT 1
    """, (course_id, student_id))

    return cursor.fetchone() is not None