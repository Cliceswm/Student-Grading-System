import bcrypt
from repositories.users_repository import (
    fetch_all_users, 
    insert_user,
    find_user_by_email_excluding,
    update_user_admin,
    update_user_password,
    get_user_by_id as repo_get_user_by_id
)


def get_user_by_id(user_id):
    return repo_get_user_by_id(user_id)


def get_all_users():
    return fetch_all_users()


def create_user(first_name: str, last_name: str, email: str, password: str, role: str):
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    success, error = insert_user(first_name, last_name, email, hashed, role)

    if not success:
        return None, error

    return "User created", None


def admin_update_user(user_id, first_name, last_name, email, role, status, new_password):
    user = get_user_by_id(user_id)
    if not user:
        return None, "User not found"

    existing = find_user_by_email_excluding(email, user_id)
    if existing:
        return None, "This email is already in use"

    no_changes = (
        user["first_name"] == first_name and
        user["last_name"] == last_name and
        user["email"] == email and
        user["role"] == role and
        user["active"] == status and
        not new_password
    )

    if no_changes:
        return None, None

    update_user_admin(user_id, first_name, last_name, email, role, status)

    if new_password:
        hashed = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        update_user_password(user_id, hashed)

    return "User updated successfully", None