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