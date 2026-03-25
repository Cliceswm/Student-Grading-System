import sqlite3
from db import get_db

def add_assessment_repo(course_id, title, description, weight, due_date):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO assessments (course_id, title, description, weight, due_date)
        VALUES (?, ?, ?, ?, ?)
    """, (course_id, title, description, weight, due_date))

    db.commit()
    return cursor.lastrowid


def get_assessments_for_course(course_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT id, course_id, title, description, weight, due_date
        FROM assessments
        WHERE course_id = ?
        ORDER BY id ASC
    """, (course_id,))

    rows = cursor.fetchall()

    return [
        {
            "id": r["id"],
            "course_id": r["course_id"],
            "title": r["title"],
            "description": r["description"],
            "weight": r["weight"],
            "due_date": r["due_date"]
        }
        for r in rows
    ]


def get_assessment_by_id(assessment_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT *
        FROM assessments
        WHERE id = ?
    """, (assessment_id,))

    return cursor.fetchone()


def assessment_title_exists(course_id, title):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT 1
        FROM assessments
        WHERE course_id = ? AND LOWER(title) = LOWER(?)
        LIMIT 1
    """, (course_id, title))

    return cursor.fetchone() is not None


def get_total_weight_for_course(course_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(weight), 0) AS total
        FROM assessments
        WHERE course_id = ?
    """, (course_id,))

    row = cursor.fetchone()
    return row["total"] if row else 0


def update_assessment_repo(assessment_id, title, description, weight, due_date):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        UPDATE assessments
        SET title = ?, description = ?, weight = ?, due_date = ?
        WHERE id = ?
    """, (title, description, weight, due_date, assessment_id))

    db.commit()
