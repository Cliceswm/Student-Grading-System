import sqlite3
from db import get_db


def find_user_by_email(email: str):
    db = get_db()
    return db.execute(
        "SELECT * FROM users WHERE LOWER(email) = LOWER(?)",
        (email,)
    ).fetchone()


def find_user_by_id(user_id: int):
    db = get_db()
    return db.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()



def fetch_all_users():
    db = get_db()
    return db.execute("SELECT * FROM users").fetchall()


def insert_user(first_name: str, last_name: str, email: str, password: str, role: str):
    db = get_db()

    try:
        db.execute("""
            INSERT INTO users (first_name, last_name, email, password, role, active)
            VALUES (?, ?, ?, ?, ?, 1)
        """, (first_name, last_name, email, password, role))

        db.commit()
        return True, None

    except sqlite3.IntegrityError:
        return False, "Email already exists"
    

def get_user_by_id(user_id):
    db = get_db()
    return db.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()


def find_user_with_email(email: str, exclude_user_id: int):
    db = get_db()
    return db.execute(
        "SELECT id FROM users WHERE LOWER(email)=LOWER(?) AND id != ?",
        (email, exclude_user_id)
    ).fetchone()


def update_user_email(user_id: int, new_email: str):
    db = get_db()
    db.execute(
        "UPDATE users SET email = ? WHERE id = ?",
        (new_email, user_id)
    )
    db.commit()


def update_user_password(user_id: int, new_password: str):
    db = get_db()
    db.execute(
        "UPDATE users SET password = ? WHERE id = ?",
        (new_password, user_id)
    )
    db.commit()


def find_user_by_email_excluding(email, user_id):
    db = get_db()
    return db.execute(
        "SELECT * FROM users WHERE email = ? AND id != ?",
        (email, user_id)
    ).fetchone()


def update_user_admin(user_id, first_name, last_name, email, role, active):
    db = get_db()
    db.execute(
        """
        UPDATE users
        SET first_name = ?, last_name = ?, email = ?, role = ?, active = ?
        WHERE id = ?
        """,
        (first_name, last_name, email, role, active, user_id)
    )
    db.commit()


def update_user_password(user_id, new_password):
    db = get_db()
    db.execute(
        "UPDATE users SET password = ? WHERE id = ?",
        (new_password, user_id)
    )
    db.commit()


def get_all_teachers():
    db = get_db()
    query = """
        SELECT id, first_name, last_name, active
        FROM users
        WHERE role = 'teacher'
        ORDER BY last_name, first_name
    """
    return db.execute(query).fetchall()
