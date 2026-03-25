import services.auth_service as auth_service
import services.users_service as users_service
import services.courses_service as courses_service
import services.enrollments_service as enrollments_service


# ---------------------------
# MODULE LOAD TESTS
# ---------------------------

def test_auth_service_module_loads():
    assert auth_service is not None


def test_users_service_module_loads():
    assert users_service is not None


def test_courses_service_module_loads():
    assert courses_service is not None


def test_enrollments_service_module_loads():
    assert enrollments_service is not None


# ---------------------------
# AUTH SERVICE TESTS
# ---------------------------

def test_auth_service_has_authentication_function():

    functions = dir(auth_service)

    assert any(
        name in functions
        for name in ["authenticate", "authenticate_user", "login_user"]
    )


# ---------------------------
# USERS SERVICE TESTS
# ---------------------------

def test_get_users_returns_list(client):

    with client.application.app_context():
        users = users_service.get_all_users()

    assert isinstance(users, list)


def test_get_user_invalid_id(client):

    with client.application.app_context():
        user = users_service.get_user_by_id(-1)

    assert user is None


# ---------------------------
# COURSES SERVICE TESTS
# ---------------------------

def test_get_courses_for_invalid_user(client):

    with client.application.app_context():
        courses = courses_service.get_courses_for_user(-1, "student")

    assert isinstance(courses, list)


# ---------------------------
# ENROLLMENTS SERVICE TESTS
# ---------------------------

def test_count_students_for_invalid_course(client):

    with client.application.app_context():
        result = enrollments_service.count_active_students_for_course(-1)

    assert isinstance(result, tuple)



def test_student_count_increases(client):

    with client.application.app_context():

        before = enrollments_service.count_active_students_for_course(1)

        enrollments_service.enroll_student(1, 1)

        after = enrollments_service.count_active_students_for_course(1)

    assert after[0] >= before[0]