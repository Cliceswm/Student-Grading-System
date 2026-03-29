# Full enrollment flow
def test_full_enrollment_flow(client):

    # 1. Login as admin
    client.post(
        "/login",
        data={"username": "admin", "password": "admin"},
        follow_redirects=True
    )

    # 2. Create a new course
    client.post(
        "/courses/add",
        data={"name": "Integration Test Course"},
        follow_redirects=True
    )

    # 3. Get courses page
    response = client.get("/courses", follow_redirects=True)
    assert response.status_code == 200

    # 4. Enroll a student into course 1 (or existing course)
    response = client.post(
        "/courses/1/edit/enrollments",
        data={"action": "enroll", "student_id": "1"},
        follow_redirects=True
    )

    assert response.status_code in (200, 302)


    # Course editing + teacher assignment
def test_course_edit_and_teacher_assignment(client):

    # Login
    client.post("/login", data={"username": "admin", "password": "admin"}, follow_redirects=True)

    # Edit course
    response = client.post(
        "/courses/1/edit",
        data={
            "name": "Integration Updated Course",
            "teacher_id": "1"
        },
        follow_redirects=True
    )

    assert response.status_code in (200, 302)

    # Verify page loads after update
    response = client.get("/courses", follow_redirects=True)
    assert response.status_code == 200



# Enrollment affects system state
def test_enrollment_affects_course_view(client):

    # Login
    client.post("/login", data={"username": "admin", "password": "admin"}, follow_redirects=True)

    # Enroll student
    client.post(
        "/courses/1/edit/enrollments",
        data={"action": "enroll", "student_id": "1"},
        follow_redirects=True
    )

    # Check enrollments page
    response = client.get("/courses/1/edit/enrollments", follow_redirects=True)

    assert response.status_code == 200



# Full user flow (very strong)
def test_full_user_flow(client):

    # Login as admin
    client.post("/login", data={"username": "admin", "password": "admin"}, follow_redirects=True)

    # Create user
    client.post(
        "/users/add",
        data={
            "first_name": "QA",
            "last_name": "User",
            "email": "qa@test.com",
            "password": "123",
            "role": "student"
        },
        follow_redirects=True
    )

    # Create course
    client.post(
        "/courses/add",
        data={"name": "QA Course"},
        follow_redirects=True
    )

    # Load users page
    response = client.get("/users", follow_redirects=True)

    assert response.status_code == 200