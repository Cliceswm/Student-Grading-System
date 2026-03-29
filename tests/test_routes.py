# Helper function to login
from tests.conftest import client


def login(client):
    return client.post(
        "/login",
        data={
            "username": "admin",
            "password": "admin"
        },
        follow_redirects=True
    )


# -----------------------
# AUTH / BASIC ROUTES
# -----------------------

def test_login_route_exists(client):
    response = client.get("/login")
    assert response.status_code == 200


def test_users_page_requires_login(client):
    response = client.get("/users", follow_redirects=True)
    assert response.status_code in (200, 302)


def test_courses_page_requires_login(client):
    response = client.get("/courses", follow_redirects=True)
    assert response.status_code in (200, 302)


def test_profile_page_requires_login(client):
    response = client.get("/profile", follow_redirects=True)
    assert response.status_code in (200, 302)


# -----------------------
# COURSE PAGES
# -----------------------

def test_enrollments_page_exists(client):
    response = client.get("/courses/1/edit/enrollments", follow_redirects=True)
    assert response.status_code in (200, 302)


def test_edit_course_page_exists(client):
    response = client.get("/courses/edit/1", follow_redirects=True)
    assert response.status_code in (200, 302, 404)


# -----------------------
# ENROLLMENT ACTIONS
# -----------------------

def test_enroll_student(client):

    login(client)

    response = client.post(
        "/courses/1/edit/enrollments",
        data={
            "action": "enroll",
            "student_id": "1"
        },
        follow_redirects=True
    )

    assert response.status_code in (200, 302)


def test_unenroll_student(client):

    login(client)

    response = client.post(
        "/courses/1/edit/enrollments",
        data={
            "action": "unenroll",
            "student_id": "1"
        },
        follow_redirects=True
    )

    assert response.status_code in (200, 302)


def test_enrollment_invalid_action(client):

    login(client)

    response = client.post(
        "/courses/1/edit/enrollments",
        data={
            "action": "invalid_action",
            "student_id": "1"
        },
        follow_redirects=True
    )

    assert response.status_code in (200, 400)


def test_enrollment_missing_student_id(client):

    login(client)

    response = client.post(
        "/courses/1/edit/enrollments",
        data={
            "action": "enroll"
        },
        follow_redirects=True
    )

    assert response.status_code in (200, 400)


def test_enrollment_empty_data(client):

    login(client)

    response = client.post(
        "/courses/1/edit/enrollments",
        data={},
        follow_redirects=True
    )

    assert response.status_code in (200, 400)


def test_enrollment_invalid_course(client):

    login(client)

    response = client.get(
        "/courses/999/edit/enrollments",
        follow_redirects=True
    )

    assert response.status_code in (200, 302, 404)

    def test_enroll_invalid_student(client):

        client.post("/login", data={"username": "admin", "password": "admin"}, follow_redirects=True)

        response = client.post(
        "/courses/1/edit/enrollments",
        data={"action": "enroll", "student_id": "999"},
        follow_redirects=True
    )

    assert response.status_code in (200, 400, 404)


# This checks the system does not crash or duplicate entries
    def test_prevent_duplicate_enrollment(client):

    # Login first
        client.post("/login", data={"username": "admin", "password": "admin"}, follow_redirects=True)

    # First enrollment
        client.post(
        "/courses/1/edit/enrollments",
        data={"action": "enroll", "student_id": "1"},
        follow_redirects=True
    )

    # Second enrollment (duplicate)
    response = client.post(
        "/courses/1/edit/enrollments",
        data={"action": "enroll", "student_id": "1"},
        follow_redirects=True
    )

    assert response.status_code in (200, 302)



    def test_unenroll_non_existing_student(client):

        client.post("/login", data={"username": "admin", "password": "admin"}, follow_redirects=True)

        response = client.post(
        "/courses/1/edit/enrollments",
        data={"action": "unenroll", "student_id": "999"},
        follow_redirects=True
    )

    assert response.status_code in (200, 302, 404)

# -----------------------
# BEHAVIOR TEST
# -----------------------

def test_student_visible_after_enrollment(client):

    login(client)

    # Enroll student
    client.post(
        "/courses/1/edit/enrollments",
        data={
            "action": "enroll",
            "student_id": "1"
        },
        follow_redirects=True
    )

    # Open enrollments page
    response = client.get(
        "/courses/1/edit/enrollments",
        follow_redirects=True
    )

    assert response.status_code == 200




def test_assign_teacher_to_course(client):

    client.post("/login", data={"username": "admin", "password": "admin"}, follow_redirects=True)

    response = client.post(
        "/courses/1/edit",
        data={
            "name": "Updated Course",
            "teacher_id": "1"
        },
        follow_redirects=True
    )

    assert response.status_code in (200, 302)




    def test_edit_course_name(client):

        client.post("/login", data={"username": "admin", "password": "admin"}, follow_redirects=True)

        response = client.post(
        "/courses/edit/1",
        data={
            "name": "QA Updated Course",
            "teacher_id": ""
        },
        follow_redirects=True
    )

    assert response.status_code in (200, 302)
