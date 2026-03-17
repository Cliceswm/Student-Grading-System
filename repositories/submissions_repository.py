from db import get_db
from datetime import date

def get_submission(assessment_id, student_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT assessment_id, student_id, submitted, student_comment, grade, feedback
        FROM submissions
        WHERE assessment_id = ? AND student_id = ?
    """, (assessment_id, student_id))

    row = cursor.fetchone()
    return dict(row) if row else None


def create_or_update_submission(assessment_id, student_id, comment):
    db = get_db()
    cursor = db.cursor()

    submitted = date.today().strftime("%Y-%m-%d")

    cursor.execute("""
        INSERT INTO submissions (assessment_id, student_id, submitted, student_comment)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(assessment_id, student_id)
        DO UPDATE SET
            submitted = excluded.submitted,
            student_comment = excluded.student_comment
    """, (assessment_id, student_id, submitted, comment))

    db.commit()


def get_submissions_for_assessment(assessment_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT 
            s.assessment_id,
            s.student_id,
            s.submitted,
            s.student_comment,
            s.grade,
            s.feedback
        FROM submissions s
        WHERE s.assessment_id = ?
    """, (assessment_id,))

    return [dict(row) for row in cursor.fetchall()]


def get_submission_student_ids(assessment_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT student_id
        FROM submissions
        WHERE assessment_id = ?
    """, (assessment_id,))

    return {row["student_id"] for row in cursor.fetchall()}


def update_submission_grade(assessment_id, student_id, grade, feedback):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        UPDATE submissions
        SET grade = ?, feedback = ?
        WHERE assessment_id = ? AND student_id = ?
    """, (grade, feedback, assessment_id, student_id))

    db.commit()
