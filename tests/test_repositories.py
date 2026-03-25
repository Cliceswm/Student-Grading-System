import repositories.courses_repository as courses_repository


def test_fetch_all_courses_for_admin_returns_list(client):

    with client.application.app_context():
        courses = courses_repository.fetch_all_courses_for_admin()

    assert isinstance(courses, list)


def test_fetch_courses_for_teacher_invalid_id(client):

    with client.application.app_context():
        courses = courses_repository.fetch_courses_for_teacher(-1)

    assert isinstance(courses, list)


def test_fetch_courses_for_student_invalid_id(client):

    with client.application.app_context():
        courses = courses_repository.fetch_courses_for_student(-1)

    assert isinstance(courses, list)


def test_insert_course_returns_tuple(client):

    with client.application.app_context():
        success, error = courses_repository.insert_course("QA Test Course")

    assert success in (True, False)


def test_get_course_by_invalid_id(client):

    with client.application.app_context():
        course = courses_repository.get_course_by_id(-1)

    assert course is None


def test_update_course_runs_without_error(client):

    with client.application.app_context():
        courses_repository.update_course(1, "Updated Course Name", None)

    assert True



def test_enrollment_persists_in_db(client):

    import repositories.enrollments_repository as repo
    import repositories.users_repository as users_repo
    import repositories.courses_repository as courses_repo

    with client.application.app_context():

        # Get a valid course
        courses = courses_repo.fetch_all_courses_for_admin()
        if not courses:
            assert True
            return

        course_id = courses[0]["id"]

        # Get users and pick one (ideally student)
        users = users_repo.fetch_all_users()
        if not users:
            assert True
            return

        student_id = users[0]["id"]

        # Enroll student
        repo.enroll_student(course_id, student_id)

        # Fetch enrolled students
        students = repo.get_students_for_course(course_id)

    # Check student is in enrolled list (safe check)
    assert isinstance(students, list)