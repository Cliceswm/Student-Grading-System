import sqlite3
import bcrypt

conn = sqlite3.connect("db.sqlite")
cursor = conn.cursor()

# Users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    active INTEGER NOT NULL DEFAULT 1,
    role TEXT NOT NULL CHECK(role IN ('student', 'teacher', 'admin'))
)
""")

# Courses table
cursor.execute("""
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    teacher_id INTEGER,
    FOREIGN KEY (teacher_id) REFERENCES users(id)
)
""")

# Enrollments table
cursor.execute("""
CREATE TABLE IF NOT EXISTS enrollments (
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY(student_id) REFERENCES users(id),
    FOREIGN KEY(course_id) REFERENCES courses(id)
)
""")

# Assessments table
cursor.execute("""
CREATE TABLE IF NOT EXISTS assessments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    weight REAL NOT NULL,
    due_date TEXT,
    FOREIGN KEY (course_id) REFERENCES courses(id)
)
""")

# Submissions table
cursor.execute("""
CREATE TABLE IF NOT EXISTS submissions (
    assessment_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    submitted TEXT NOT NULL,
    student_comment TEXT,
    grade REAL,
    feedback TEXT,
    PRIMARY KEY (assessment_id, student_id),
    FOREIGN KEY (assessment_id) REFERENCES assessments(id),
    FOREIGN KEY (student_id) REFERENCES users(id)
)
""")

# Create admin if not exists
cursor.execute("SELECT * FROM users WHERE role = 'admin'")
admin_exists = cursor.fetchone()

if not admin_exists:
    raw_password = "admin123"
    hashed = bcrypt.hashpw(raw_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    cursor.execute("""
        INSERT INTO users (first_name, last_name, email, password, role)
        VALUES (?, ?, ?, ?, ?)
    """, ("Admin", "Adminych", "admin@example.com", hashed, "admin"))

    print(f"Administrator created: admin@example.com / {raw_password} (hashed)")
else:
    print("Administrator exists")

conn.commit()
conn.close()

print("Database created!")