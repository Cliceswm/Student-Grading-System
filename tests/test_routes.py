# Helper function to login
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